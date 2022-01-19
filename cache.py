

from mimetypes import init




class cache:
    def __init__(self, CACHE_SIZE = 100, method="FIFO"):  
        self.CACHE_SIZE = CACHE_SIZE
        self.CACHE_METHOD = method



    def start_caching(self):
        if self.CACHE_METHOD == "FIFO":
            self.FIFO()
        elif self.CACHE_METHOD == "LIFO":
            self.LIFO()
        elif self.CACHE_METHOD == "LRU":
            self.LRU()
        elif self.CACHE_METHOD == "LFU":
            self.LFU()
        else:
            return "error"
        return 0


    def FIFO(self):
        return 0
    
    def LIFO(self):
        return 0
    
    def LRU(self):
        return 0

    def LFU(self):
        return 0