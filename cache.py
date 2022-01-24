from mimetypes import init
from time import clock_gettime

class cache:
    def __init__(self, page_requests, cache_size = 100, method="FIFO"):  
        self.PAGE_REQUESTS = page_requests
        self.CACHE_SIZE = cache_size
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

        
        self.LFD()
        return 0


    def FIFO(self):
        return 0
    
    def LIFO(self):
        return 0
    
    def LRU(self):
        return 0

    def LFU(self):
        return 0
    
    def LFD(self):
        return 0



if __name__ == "__main__":
    n = 100
    print("hi")