from collections import deque
from lru_list import LRUList


class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = set()
        self.elements = deque()
        self.misses = 0

    def get(self, page):
        if page not in self.cache:
            self.misses += 1
            if len(self.cache) == self.capacity:
                self.cache.remove(self.elements.popleft())
            self.elements.append(page)
            self.cache.add(page)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "FIFO"


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = LRUList()
        self.misses = 0

    def get(self, page):
        if not self.cache.contains(page):
            self.misses += 1
            if self.cache.size() == self.capacity:
                self.cache.pop()
        self.cache.move_mru(page)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "LRU"
