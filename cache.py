from mimetypes import init
from time import clock_gettime, sleep
import random

PAGE_NUM = 20
PAGE_REQUEST_NUM = 100
CACHE_SIZE = 5

class cache:
    def __init__(self, page_num, page_request_count, cache_size = 100):
        # number of distinct pages
        self.page_num = page_num
        # number of page requests
        self.page_request_count = page_request_count
        # the size of cache
        self.cache_size = cache_size
        # a series of page requests
        self.requests = None

    # setter for page_num, page_request_count, and cache_size
    def reset_test_values(self, total_page_num, page_request_count, cache_size):
        self.page_num = total_page_num
        self.page_request_count = page_request_count
        self.cache_size = cache_size        

    # randomly generate a series of page requests, and set the page requests
    def generate_requests(self):
        requests = []
        for _ in range(self.page_request_count):
            requests.append(random.randint(1, self.page_num))
        
        self.set_requests(requests)

    # setter for page requests
    def set_requests(self, requests):
        self.requests = requests

    # simulate a cache with a First In First Out caching Policy
    def FIFO(self):
        summary = open("FIFO_output.txt", "w")
        summary.write("FIFO cache with page requests:\n" + str(self.requests) + "\n\n")        

        cache = []
        miss_count = 0
        for i in range(self.page_request_count):
            page = self.requests[i]
            if page not in cache:
                miss_count += 1
                if len(cache) == self.cache_size:
                    cache = cache[1:]
                    
                cache.append(page)
                summary.write("Cache miss! Current Cache: " + str(cache) + "\n")
            else:
                summary.write("Cache hit on page " + str(page) + "! Current Cache: " + str(cache) + "\n")

        summary.write("\nTotal miss count: "  + str(miss_count) +" out of " + str(self.page_request_count) + " requests.\n")
        summary.close()
    
    def LIFO(self):
        return 0
    
    def LRU(self):
        return 0

    def LFU(self):
        return 0
    
    def LFD(self):
        return 0


    def set_cache_size(self, cache_size):
        self.CACHE_SIZE = cache_size

    def set_request_page_count(self, page_request_count):
        self.PAGE_REQUESTS_COUNT = page_request_count


if __name__ == "__main__":
    mycache = cache(PAGE_NUM, PAGE_REQUEST_NUM, CACHE_SIZE)
    mycache.generate_requests()
    mycache.FIFO()