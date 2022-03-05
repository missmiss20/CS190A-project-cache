# a fixed-size array of "pages" that supports access/mutation/retrieval
# each index represents a page; in order to operate on an index, we simulate bringing it into memory
from math import ceil, sqrt


class CachedArray:

    def __init__(self, elements, cache, cache_line=1, offset=0):
        self.cache = cache
        self.elements = elements
        self.cache_line = cache_line
        self.offset = 0

    def get(self, index):
        self.cache.get(self.offset + (index // self.cache_line))  # simulate retrieving the page from cache
        return self.elements[index]

    def put(self, index, val):
        self.cache.get(self.offset + (index // self.cache_line))
        self.elements[index] = val

    def reverse(self, i, j):
        while i < j:
            self.swap(i, j)
            i += 1
            j -= 1

    def swap(self, i, j):
        tmp = self.get(i)
        self.put(i, self.get(j))
        self.put(j, tmp)

    def get_cache_misses(self):
        return self.cache.get_cache_misses()

    def get_arr(self):
        return self.elements

# wrapper around CachedArray that makes indexing a little easier


class Cached2DArray:

    def __init__(self, elements, cache, cache_line=1, offset=0):
        self.cache = CachedArray(elements, cache, cache_line, offset)
        self.n = ceil(sqrt(len(elements)))

    def get(self, row, col):
        return self.cache.get(row * self.n + col)

    def put(self, row, col, val):
        self.cache.put(row * self.n + col, val)

    def get_cache_misses(self):
        return self.cache.get_cache_misses()

    def get_arr(self):
        return self.elements
