# a fixed-size array of "pages" that supports access/mutation/retrieval
# each index represents a page; in order to operate on an index, we simulate bringing it into memory
from cmath import sqrt


class CachedArray:

    def __init__(self, elements, cache):
        self.cache = cache
        self.elements = elements

    def get(self, index):
        self.cache.get(index)  # simulate retrieving the page from cache
        return self.elements[index]

    def put(self, index, val):
        self.cache.get(index)
        self.elements[index] = val

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

    def __init__(self, elements, cache):
        self.cache = CachedArray(elements, cache)
        self.n = sqrt(len(elements))

    def get(self, row, col):
        return self.cache.get(row * self.n + col)

    def put(self, row, col, val):
        self.cache.put(row * self.n + col, val)

    def get_cache_misses(self):
        return self.cache.get_cache_misses()

    def get_arr(self):
        return self.elements
