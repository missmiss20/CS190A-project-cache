from collections import defaultdict, deque
from mimetypes import init
from xmlrpc.client import MAXINT
from sortedcontainers import SortedSet
#from time import clock_gettime, sleep
import random

from query_generator import *

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
    
    # three output writter functions
    def get_output_handle(self, policy):
        summary = open(f"{policy}_output.txt", "w")
        summary.write(f"{policy} cache with page requests:\n{self.requests}\n\n")
        return summary
        
    def write_action(self, miss, page, cache, summary):
        if miss:
            summary.write("Cache miss!")
        else:
            summary.write(f"Cache hit on page {page}!")
        summary.write(f" Current Cache: {cache}\n")
    
    def write_summary(self, miss_count, summary):
        summary.write(f"\nTotal miss count: {miss_count} out of {self.page_request_count} requests.\n")

    # simulate a cache with a First In First Out caching Policy
    def FIFO(self):
        summary = self.get_output_handle("FIFO")

        cache = []
        miss_count = 0
        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache:
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size:
                    cache = cache[1:]
                    
                cache.append(page)

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        summary.close()
        return miss_count
    
    # simulate a cache with a Last In First Out caching Policy
    def LIFO(self):
        summary = self.get_output_handle("LIFO")
        
        cache = []
        miss_count = 0
        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache:
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size:
                    cache = cache[0:-1]
                    
                cache.append(page)

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        summary.close()
        return miss_count
    
    #use array of size self.cache_size, simiar to FIFO except add to front of list and move page number to front of list on cache hit
    #on cache miss with full cache, remove last element of list (least recent access) and insert new page to front
    def LRU(self):
        summary = self.get_output_handle("LRU")

        cache = []
        miss_count = 0

        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache: #add to front, if needed remove last element
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size: #cache full, remove last element
                    cache = cache[:-1]
                    
                cache.insert(0, page) #add to front, push everything else back
            else: #move page from current location to front
                cache.remove(page)
                cache.insert(0,page)

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        summary.close()
        return miss_count


    # simulate a cache with a Least Frequently Used caching Policy
    def LFU(self):
        summary = self.get_output_handle("LFU")

        cache = []
        page_amount = dict()
        miss_count = 0
        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache:
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size:
                    LFU_count = MAXINT
                    for element in page_amount:
                        if LFU_count > page_amount[element]:
                            LFU_count = page_amount[element]
                            LFU_page = element
                    
                    cache.remove(LFU_page)
                    page_amount.pop(LFU_page)
                    
                cache.append(page)
                page_amount[page] = 1
            else:
                page_amount[page] += 1
            
            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        summary.close()
        return miss_count
    
    # LFD in O(NlogK) time, where N is the number of requests and K is the cache size
    def LFD(self):
        summary = self.get_output_handle("LFD")

        # Precalculate indices of each page
        occurrences = defaultdict(lambda : deque())
        for i in range(self.page_request_count):
            occurrences[self.requests[i]].append(i)
            
        next_occurrence = lambda page : occurrences[page][0] if len(occurrences[page]) > 0 else float('inf')

        cache = set()
        prio_set = SortedSet() # contains (next_occurrence, page)
        miss_count = 0
        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            occurrences[page].popleft()
            if page not in cache:
                miss_count += 1
                miss = True
                if len(cache) == self.cache_size:
                    cache.remove(prio_set.pop()[1])
                cache.add(page)
            else:
                prio_set.remove((i, page))
            prio_set.add((next_occurrence(page), page))

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary) 
        summary.close()
        return miss_count

    # simulate a cache with a Random page eviction Policy
    # if cache is full evict random page to replace with the new one
    def Random(self):
        summary = self.get_output_handle("Random")

        cache = []
        miss_count = 0
        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache:
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size:
                    index = random.randint(0, self.cache_size - 1)
                    cache[index] = page
                    
                else:
                    cache.append(page)

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        summary.close()
        return miss_count

    def set_cache_size(self, cache_size):
        self.CACHE_SIZE = cache_size

    def set_request_page_count(self, page_request_count):
        self.PAGE_REQUESTS_COUNT = page_request_count


if __name__ == "__main__":
    mycache = cache(PAGE_NUM, PAGE_REQUEST_NUM, CACHE_SIZE)
    mycache.generate_requests()
    mycache.FIFO()
    mycache.LIFO()
    mycache.LFD()
    mycache.LFU()
    mycache.Random()
    mycache.LRU()
