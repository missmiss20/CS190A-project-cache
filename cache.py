from mimetypes import init
from time import clock_gettime
import random

class cache:
    def __init__(self, total_page_num, page_request_count, cache_size = 100):
        self.total_page_num = total_page_num
        self.page_request_count = page_request_count
        self.cache_size = cache_size
        self.requests = self.generate_requests(total_page_num, page_request_count)


    def reset_test_values(self, total_page_num, page_request_count, cache_size):
        self.total_page_num = total_page_num
        self.page_request_count = page_request_count
        self.cache_size = cache_size        

    def generate_requests(self):
        output = []
        for _ in range(self.page_request_count):
            output.append(random.randint(1, self.total_page_num))

        self.requests = output


    def start_caching(self, method):
        if method == "FIFO":
            self.FIFO()
        elif method == "LIFO":
            self.LIFO()
        elif method == "LRU":
            self.LRU()
        elif method == "LFU":
            self.LFU()
        elif method == "LFD":
            self.LFD()
        else:
            print("Error: Please input a valid caching method")

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


    def set_cache_size(self, cache_size):
        self.CACHE_SIZE = cache_size

    def set_request_page_count(self, page_request_count):
        self.PAGE_REQUESTS_COUNT = page_request_count



if __name__ == "__main__":
    n = 100
    print("hi")