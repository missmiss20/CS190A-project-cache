from cached_ds import CachedArray
from caches import FIFOCache, LRUCache
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


if __name__ == "__main__":

    fifo_res = []
    lru_res = []
    for _ in range(100):
        fifo_arr = [*range(100)]
        random.shuffle(fifo_arr)
        lru_arr = fifo_arr.copy()  # we want to see performance on same input
        # print(f"original unsorted: {fifo_arr}")
        fifo_res.append(cached_quicksort(fifo_arr, FIFOCache(10)))
        lru_res.append(cached_quicksort(lru_arr, LRUCache(10)))
        # print(f"fifo misses: {fifo_res[-1]}")
        # print(f"lru misses: {lru_res[-1]}")
        
    fig, ax = plt.subplots()
    ax.plot([*range(100)], fifo_res, color="red", marker="o")
    ax.set_xlabel("iteration")
    ax.set_ylabel("cache misses")
    ax2 = ax.twinx()
    ax2.plot([*range(100)], lru_res, color="blue", marker="o")
    fig.savefig('quicksort_results.jpg', format='jpeg')

    fifo_better = 0
    largest_delta = -float('inf')
    smallest_delta = float('inf')
    for i in range(100):
        if fifo_res[i] < lru_res[i]:
            fifo_better += 1
        largest_delta = max(largest_delta, fifo_res[i] - lru_res[i])
        smallest_delta = min(smallest_delta, fifo_res[i] - lru_res[i])
    print(f"fifo outperforms lru on {fifo_better} out of {100} iterations, {fifo_better / 100}%")
    print(f"fifo beat lru by a maximum of {largest_delta} cache misses")
    print(f"lru beat fifo by a maximum of {-smallest_delta} cache misses")


