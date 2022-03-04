from math import floor
from cached_ds import CachedArray
from caches import ARCache, FIFOCache, LRUCache
import concurrent.futures
import random
import matplotlib.pyplot as plt


def cached_quicksort(arr, cache):
    cached_arr = CachedArray(arr, cache)

    def partition(cached_arr, lo, hi):
        i = lo - 1
        pivot = cached_arr.get(hi)  # take last element as pivot
        for j in range(lo, hi):
            if cached_arr.get(j) <= pivot:
                i += 1
                tmp = cached_arr.get(i)
                cached_arr.put(i, cached_arr.get(j))
                cached_arr.put(j, tmp)
        tmp = cached_arr.get(i + 1)
        cached_arr.put(i + 1, cached_arr.get(hi))
        cached_arr.put(hi, tmp)
        return i + 1

    def quicksort(cached_arr, lo, hi):
        if lo < hi:
            pivot = partition(cached_arr, lo, hi)
            quicksort(cached_arr, lo, pivot - 1)
            quicksort(cached_arr, pivot + 1, hi)

    quicksort(cached_arr, 0, len(arr) - 1)
    return cached_arr.get_cache_misses()

# add new caches here


def get_caches(capacity):
    return [ARCache(capacity), FIFOCache(capacity), LRUCache(capacity)]


if __name__ == "__main__":

    CACHE_SIZES = [0.1, 0.25, 0.5, 0.75]
    ITERATIONS = 100
    INPUT_SIZE = 100

    NUM_CACHES = len(get_caches(0))
    CACHE_NAMES = [cache.name() for cache in get_caches(0)]

    # quicksort benchmarks
    # { algo: [avg_on_cache_sizes[0], ...] }
    # avg_misses_by_cache_size = {}
    for cache_sz_percentage in CACHE_SIZES:
        # total_cache_misses_per_cache = {}
        cache_size = floor(INPUT_SIZE * cache_sz_percentage)

        results = [[] for _ in range(NUM_CACHES)]

        # score_mat[i][j] = k means that cache i beat cache j k times
        score_mat = [[0 for _ in range(NUM_CACHES)] for _ in range(NUM_CACHES)]

        for _ in range(ITERATIONS):
            arr = [*range(INPUT_SIZE)]
            random.shuffle(arr)
            caches = get_caches(cache_size)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(
                    cached_quicksort, arr=arr.copy(), cache=cache): i for (i, cache) in enumerate(caches)}
                for future in concurrent.futures.as_completed(futures):
                    results[futures[future]].append(future.result())

            for i in range(NUM_CACHES):
                for j in range(NUM_CACHES):
                    score_mat[i][j] += 1 if results[i][-1] < results[j][-1] else 0

        fig, ax = plt.subplots()
        ax.boxplot(results)
        ax.set_title(f"Quicksort cache miss distribution with k={cache_size}")
        ax.set_xticklabels(CACHE_NAMES)
        ax.set_ylabel("Cache misses")
        fig.savefig(f"qs{cache_size}.jpg", format="jpeg")

        fig, ax = plt.subplots()
        im = ax.imshow(score_mat, cmap="YlGn")
        ax.set_title(f"Quicksort score comparison with k={cache_size}")
        ax.set_xticks(range(NUM_CACHES), labels=CACHE_NAMES)
        ax.set_yticks(range(NUM_CACHES), labels=CACHE_NAMES)
        for i in range(NUM_CACHES):
            for j in range(NUM_CACHES):
                text = ax.text(
                    j, i, score_mat[i][j] / ITERATIONS, ha="center", va="center")
        fig.savefig(f"qs_score{cache_size}.jpg", format="jpeg")
