from math import ceil
from cached_ds import CachedArray, Cached2DArray
from caches import ARCache, FIFOCache, LFUCache, LIFOCache, LRUCache, RandomCache, Random1BitLRUCache
import concurrent.futures
import os
import random
import matplotlib.pyplot as plt
import time


def cached_quicksort(ins, cache):
    cached_arr = CachedArray(ins, cache)

    def partition(cached_arr, lo, hi):
        i = lo - 1
        pivot = cached_arr.get(hi)  # take last element as pivot
        for j in range(lo, hi):
            if cached_arr.get(j) <= pivot:
                i += 1
                cached_arr.swap(i, j)
        cached_arr.swap(i + 1, hi)
        return i + 1

    def quicksort(cached_arr, lo, hi):
        if lo < hi:
            pivot = partition(cached_arr, lo, hi)
            quicksort(cached_arr, lo, pivot - 1)
            quicksort(cached_arr, pivot + 1, hi)

    quicksort(cached_arr, 0, len(ins) - 1)
    return cached_arr.get_cache_misses()


def cached_dfs(ins, cache):
    cached_arr = CachedArray([i for i in range(len(ins))], cache)

    def dfs(node, cached_nodes, tree):
        cached_nodes.get(node)
        for adj in tree[node]:
            dfs(adj, cached_nodes, tree)
            # everytime we come back up, we need to get this node in memory so we can check its neighbors
            cached_nodes.get(node)

    dfs(0, cached_arr, ins)
    return cached_arr.get_cache_misses()


def cached_bubblesort(ins, cache):
    cached_arr = CachedArray(ins, cache)
    for j in range(len(ins) - 1, 0, -1):
        for i in range(j):
            if cached_arr.get(i) > cached_arr.get(i + 1):
                cached_arr.swap(i, i + 1)
    return cached_arr.get_cache_misses()


# https://benchmarksgame-team.pages.debian.net/benchmarksgame/description/fannkuchredux.html
# skips checksum + counting, since we just care about running the program
def cached_fannkuch_redux(ins, cache):
    cached_arr = CachedArray(ins, cache)

    def fannkuch_redux(cached_arr):
        while cached_arr.get(0) != 1:
            cached_arr.reverse(0, cached_arr.get(0) - 1)

    n = len(ins)
    while True:
        tmp = cached_arr.get_arr().copy()
        fannkuch_redux(cached_arr)
        for i, e in enumerate(tmp):
            cached_arr.put(i, e)

        i = j = n - 1
        while i > 0 and cached_arr.get(i - 1) >= cached_arr.get(i):
            i -= 1
        if i == 0:
            return cached_arr.get_cache_misses()
        k = i - 1
        while cached_arr.get(j) <= cached_arr.get(k):
            j -= 1
        cached_arr.swap(j, k)
        cached_arr.reverse(k + 1, n - 1)


def cached_matrix_multiplication(ins, cache):
    cached_mat1 = Cached2DArray(ins[0], cache)
    cached_mat2 = Cached2DArray(ins[1], cache, offset=len(ins[0]))
    n = cached_mat1.n
    for i in range(n):
        for j in range(n):
            val = 0
            for k in range(n):
                val += cached_mat1.get(i, k) * cached_mat2.get(k, j)
    return cache.get_cache_misses()


def cached_prime_sieve(ins, cache):
    cached_arr = CachedArray(ins, cache)
    p = 2
    while p * p <= len(ins) - 1:
        if cached_arr.get(p):
            for i in range(p * p, len(ins), p):
                cached_arr.put(i, False)
        p += 1

    primes = [i for i in range(len(ins) - 1) if i >= 2 and cached_arr.get(i)]
    return cache.get_cache_misses()


def gen_shuffled_array(n):
    arr = [i for i in range(n)]
    random.shuffle(arr)
    return arr


def gen_weighted_array(n):
    arr = []
    for _ in range(n):
        # arbitrary end value, but has to be nonnegative
        arr.append(random.randint(0, n))
    return arr

# randomly generates a tree with num_nodes nodes labeled
# 0 to num_nodes, rooted at 0 in adjacency list form


def gen_tree(num_nodes):
    graph = {0: []}
    for node in range(1, num_nodes):
        parent = random.randint(0, node - 1)
        graph[parent].append(node)
        graph[node] = []

    return graph


def get_caches(capacity):
    return [ARCache(capacity), FIFOCache(capacity), LFUCache(capacity), LIFOCache(capacity), LRUCache(capacity), RandomCache(capacity), Random1BitLRUCache(capacity)]


def benchmark_algorithm(algorithm, algorithm_full, algorithm_label, input_generator, read_only=False, cache_sizes=[0.1, 0.25, 0.5, 0.75], iterations=100, input_size=100):
    os.makedirs(f"{algorithm_label}_res", exist_ok=True)
    print(f"{algorithm_full} benchmark with cache_sizes={cache_sizes}, iterations={iterations}, and input_size={input_size}")

    tstart = time.perf_counter()
    algorithm(input_generator(input_size), ARCache(1))
    tend = time.perf_counter()
    print(f"1 iteration of {algorithm_label} ran with ARC took {tend - tstart} seconds, estimated full completion time={len(cache_sizes) * iterations * (tend - tstart) * 4}")

    start = time.perf_counter()
    NUM_CACHES = len(get_caches(0))
    CACHE_NAMES = [cache.name() for cache in get_caches(0)]

    avg_misses = [[] for _ in range(NUM_CACHES)]

    for (csz, cache_sz_percentage) in enumerate(cache_sizes):
        cache_size = ceil(input_size * cache_sz_percentage)

        results = [[] for _ in range(NUM_CACHES)]

        # score_mat[i][j] = k means that cache i beat cache j k times
        score_mat = [[0 for _ in range(NUM_CACHES)] for _ in range(NUM_CACHES)]

        for i in range(NUM_CACHES):
            avg_misses[i].append(0)

        for _ in range(iterations):
            ins = input_generator(input_size)
            caches = get_caches(cache_size)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(
                    algorithm, ins=ins if read_only else ins.copy(), cache=cache): i for (i, cache) in enumerate(caches)}
                for future in concurrent.futures.as_completed(futures):
                    results[futures[future]].append(future.result())

            for i in range(NUM_CACHES):
                avg_misses[i][csz] += results[i][-1]
                for j in range(NUM_CACHES):
                    score_mat[i][j] += 1 if results[i][-1] < results[j][-1] else 0

        fig, ax = plt.subplots()
        ax.boxplot(results)
        ax.set_title(
            f"{algorithm_full} cache miss distribution with k={cache_size}")
        ax.set_xticklabels(CACHE_NAMES)
        ax.set_ylabel("Cache misses")
        fig.savefig(
            f"{algorithm_label}_res/{algorithm_label}{cache_size}.jpg", format="jpeg")
        plt.close(fig)

        fig, ax = plt.subplots()
        im = ax.imshow(score_mat, cmap="YlGn")
        ax.set_title(f"{algorithm_full} score comparison with k={cache_size}")
        ax.set_xticks(range(NUM_CACHES), labels=CACHE_NAMES)
        ax.set_yticks(range(NUM_CACHES), labels=CACHE_NAMES)
        for i in range(NUM_CACHES):
            for j in range(NUM_CACHES):
                text = ax.text(
                        j, i, f"{(score_mat[i][j] / iterations):.2f}", ha="center", va="center")
        fig.savefig(
            f"{algorithm_label}_res/{algorithm_label}_score{cache_size}.jpg", format="jpeg")
        plt.close(fig)

    for i in range(NUM_CACHES):
        for j in range(len(cache_sizes)):
            avg_misses[i][j] /= iterations

    fig, ax = plt.subplots()
    for (i, cache_name) in enumerate(CACHE_NAMES):
        line = ax.plot(cache_sizes, avg_misses[i], label=cache_name)

    ax.legend()
    ax.set_title(f"{algorithm_full} average cache misses")
    ax.set_ylabel("Cache misses")
    ax.set_xlabel("Cache size (% of input size)")
    fig.savefig(
        f"{algorithm_label}_res/{algorithm_label}_avgs.jpg", format="jpeg")
    plt.close(fig)
    end = time.perf_counter()
    print(f"{algorithm_full} benchmark finished in {end - start}s")


if __name__ == "__main__":
    benchmark_algorithm(cached_bubblesort, "Bubblesort",
                        "bs", gen_shuffled_array, iterations=10)
    benchmark_algorithm(cached_dfs, "Depth-first search",
                        "dfs", gen_tree, read_only=True, input_size=1000)
    benchmark_algorithm(cached_quicksort, "Quicksort",
                        "qs", gen_shuffled_array)
    # although input is static, want to show some distribution for random eviction policies
    benchmark_algorithm(cached_fannkuch_redux, "Fannkuch-redux",
                        "fr", lambda n: [i for i in range(1, n + 1)], iterations=3, input_size=7)
    benchmark_algorithm(cached_matrix_multiplication, "Matrix multiplication",
                        "matm", lambda n: [gen_shuffled_array(n), gen_shuffled_array(n)], iterations=5, input_size=400)
    benchmark_algorithm(cached_prime_sieve, "Prime sieve", "ps", lambda n: [
                         True] * n, iterations=3, input_size=1000)
