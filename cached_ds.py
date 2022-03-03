# a fixed-size array of "pages" that supports access/mutation/retrieval
# each index represents a page; in order to operate on an index, we simulate bringing it into memory
class CachedArray:

    def __init__(self, elements, cache):
        self.cache = cache
        self.elements = elements
    
    def get(self, index):
        self.cache.get(index) # simulate retrieving the page from cache
        return self.elements[index]
    
    def put(self, index, val):
        self.cache.get(index) 
        self.elements[index] = val

    def get_cache_misses(self):
        return self.cache.get_cache_misses()

    def get_arr(self):
        return self.elements

    

        