from collections import deque


class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = deque()
        self.misses = 0

    def get(self, page):
        if page not in self.cache:
            self.misses += 1
            if len(self.cache) == self.capacity:
                self.cache.popleft()
            self.cache.append(page)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "FIFO"


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = deque()
        self.misses = 0

    def get(self, page):
        if page in self.cache:
            self.cache.remove(page)
        else:
            self.misses += 1
            if len(self.cache) == self.capacity:
                self.cache.popleft()
        self.cache.append(page)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "LRU"

