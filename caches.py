from collections import defaultdict, deque
from llist import dllist
from lru_list import LRUList

class ARCache:
    def __init__(self, capacity):
        self.p = 0
        self.t1 = LRUList()
        self.t2 = LRUList()
        self.b1 = LRUList()
        self.b2 = LRUList()
        self.misses = 0
        self.capacity = capacity

    def replace(self, element):
        if self.t1.size() > 0 and (self.t1.size() > self.p or (self.b2.contains(element) and self.t1.size() == self.p)):
            self.b1.move_mru(self.t1.pop())
        else:
            self.b2.move_mru(self.t2.pop())

    def get(self, page):
        if self.t1.contains(page):
            self.t1.remove(page)
            self.t2.move_mru(page)
        elif self.t2.contains(page):
            self.t2.move_mru(page)
        else:
            self.misses += 1
            if self.b1.contains(page):
                self.p = min(self.p + max(1, self.b2.size() / self.b1.size()), self.capacity)
                self.replace(page)
                self.b1.remove(page)
                self.t2.move_mru(page)
            elif self.b2.contains(page):
                self.p = max(self.p - max(1, self.b1.size() / self.b2.size()), 0)
                self.replace(page)
                self.b2.remove(page)
                self.t2.move_mru(page)
            else:
                if self.t1.size() + self.b1.size() == self.capacity:
                    if self.t1.size() < self.capacity:
                        self.b1.pop()
                        self.replace(page)
                    else:
                        self.t1.pop()
                elif self.t1.size() + self.b1.size() < self.capacity:
                    total_size = self.t1.size() + self.t2.size() + self.b1.size() + self.b2.size()
                    if total_size >= self.capacity:
                        if total_size == 2 * self.capacity:
                            self.b2.pop()
                        self.replace(page)
                self.t1.move_mru(page)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "ARC"


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


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}
        self.freq = defaultdict(dllist)
        self.minfreq = 0
        self.size = 0
        self.misses = 0

    def get(self, page):
        if page in self.nodes:
            node = self.nodes[page]
            freq = node.value[1]
            self.freq[freq].remove(node)
            if self.minfreq == freq and len(self.freq[freq]) == 0:
                self.minfreq += 1
            self.nodes[page] = self.freq[freq + 1].appendright([page, freq + 1])
        else:
            self.misses += 1            
            if self.size == self.capacity:
                val = self.freq[self.minfreq].popleft()
                self.nodes.pop(val[0])
                self.size -= 1
            node = self.freq[1].appendright([page, 1])
            self.nodes[page] = node
            self.minfreq = 1
            self.size += 1
        # print(self.nodes)
        # print(self.freq)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "LFU"

class LIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = set()
        self.list = []
        self.misses = 0

    def get(self, page):
        if page not in self.cache:
            self.misses += 1
            if len(self.cache) == self.capacity:
                self.cache.remove(self.list.pop())
            self.list.append(page)
            self.cache.add(page)

    def get_cache_misses(self):
        return self.misses

    def name(self):
        return "LIFO"


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
