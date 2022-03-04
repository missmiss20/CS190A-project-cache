from llist import dllist


class LRUList:
    def __init__(self):
        self.list = dllist()
        self.cache = dict()

    def remove(self, element):
        self.list.remove(self.cache[element])
        self.cache.pop(element)

        return element

    # makes an element most recently used
    def move_mru(self, element):
        if element in self.cache:
            self.list.remove(self.cache[element])
        self.cache[element] = self.list.appendright(element)

    # evicts LRU and returns it
    def pop(self):
        lru = self.list.popleft()
        self.cache.pop(lru)
        return lru
   
    def contains(self, element):
        return element in self.cache
    
    def size(self):
        return len(self.cache)
    
    def get_cache(self):
        return self.cache
