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

    worst_fifo_misses = -float('inf')
    wfifo_arr = []
    best_fifo_misses = float('inf')
    bfifo_arr = []

    worst_lru_misses = -float('inf')
    wlru_arr = []
    best_lru_misses = float('inf')
    blru_arr = []


    largest_delta = -float('inf')
    ld_arr = []
    smallest_delta = float('inf')
    sd_arr = []
    fifo_better = 0
    lru_better = 0
    same = 0

    for _ in range(100):
        arr = [*range(100)]
        random.shuffle(arr)
        fifo_arr = arr.copy()
        lru_arr = arr.copy()  # we want to see performance on same input
        fifo_res.append(cached_quicksort(fifo_arr, FIFOCache(10)))
        lru_res.append(cached_quicksort(lru_arr, LRUCache(10)))

        if fifo_res[-1] > worst_fifo_misses:
            worst_fifo_misses = fifo_res[-1]
            wfifo_arr = arr
        elif fifo_res[-1] < best_fifo_misses:
            best_fifo_misses = fifo_res[-1]
            bfifo_arr = arr

        if lru_res[-1] > worst_lru_misses:
            worst_lru_misses = lru_res[-1]
            wlru_arr = arr
        elif lru_res[-1] < best_lru_misses:
            best_lru_misses = lru_res[-1]
            blru_arr = arr


        delta = fifo_res[-1] - lru_res[-1]
        if delta > 0:
            lru_better += 1
        elif delta == 0:
            same += 1
        else:
            fifo_better += 1
        if delta > largest_delta:
            largest_delta = delta
            ld_arr = arr
        if delta < smallest_delta:
            smallest_delta = delta
            sd_arr = arr

        
    fig, ax = plt.subplots()
    ax.plot([*range(100)], fifo_res, color="red", marker="o")
    ax.set_xlabel("iteration")
    ax.set_ylabel("cache misses")
    ax2 = ax.twinx()
    ax2.plot([*range(100)], lru_res, color="blue", marker="o")
    fig.savefig('quicksort_results.jpg', format='jpeg')

    print(f"fifo outperforms lru on {fifo_better} out of {100} iterations, {fifo_better}%")
    print(f"lru outperforms fifo on {lru_better} out of {100} iterations, {lru_better}%")
    print(f"fifo performs the same as lru on {same} out of {100} iterations, {same}%")
    print(f"lru beat fifo by a maximum of {largest_delta} cache misses, on the following permutation")
    print(ld_arr)
    print(f"fifo beat lru by a maximum of {-smallest_delta} cache misses, on the following permutation")
    print(sd_arr)

    print(f"fifo performed best with {best_fifo_misses} on the following permutation")
    print(bfifo_arr)
    print(f"fifo performed worst with {worst_fifo_misses} on the following permutation")
    print(wfifo_arr)

    print(f"lru performed best with {best_lru_misses} on the following permutation")
    print(blru_arr)
    print(f"lru performed worst with {worst_lru_misses} on the following permutation")
    print(wlru_arr)

