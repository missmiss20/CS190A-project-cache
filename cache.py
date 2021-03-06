from collections import defaultdict, deque
from mimetypes import init
from xmlrpc.client import MAXINT
from sortedcontainers import SortedSet
from lru_list import LRUList
#from time import clock_gettime, sleep
import random

from query_generator import *

PAGE_NUM = 20
PAGE_REQUEST_NUM = 100
CACHE_SIZE = 5

NORMAL_DISTRIBUTION = 1
TRIANGLE_DISTRIBUTION = 2
ARBITARY_RADIO_DISTRIBUTION = 3


class cache:
    def __init__(self, page_num, page_request_count, cache_size=100, write_to_file=True):
        # number of distinct pages
        self.page_num = page_num
        # number of page requests
        self.page_request_count = page_request_count
        # the size of cache
        self.cache_size = cache_size
        # a series of page requests
        self.requests = None
        self.write_to_file = write_to_file

    # setter for page_num, page_request_count, and cache_size
    def reset_test_values(self, total_page_num, page_request_count, cache_size):
        self.page_num = total_page_num
        self.page_request_count = page_request_count
        self.cache_size = cache_size

    # randomly generate a series of page requests, and set the page requests
    def generate_requests(self, request_type=0, ratios=[]):
        requests = []
        if request_type == 0:
            for _ in range(self.page_request_count):
                requests.append(random.randint(1, self.page_num))

        elif request_type == NORMAL_DISTRIBUTION:
            requests = generate_normal_distribution(
                self.page_num, self.page_request_count)
        elif request_type == TRIANGLE_DISTRIBUTION:
            requests = generate_triangular_distribution(
                self.page_num, self.page_request_count)
        elif request_type == ARBITARY_RADIO_DISTRIBUTION:
            requests = generate_ratio_distribution(
                self.page_num, self.page_request_count, ratios)

        self.set_requests(requests)

    # setter for page requests
    def set_requests(self, requests):
        self.requests = requests

    def set_radios(self, radios):
        self.ratios = radios

    # three output writter functions
    def get_output_handle(self, policy):
        if not self.write_to_file:
            return 0
        summary = open(f"{policy}_output.txt", "w")
        summary.write(
            f"{policy} cache with page requests:\n{self.requests}\n\n")
        return summary

    def write_action(self, miss, page, cache, summary):
        if not self.write_to_file:
            return
        if miss:
            summary.write("Cache miss!")
        else:
            summary.write(f"Cache hit on page {page}!")
        summary.write(f" Current Cache: {cache}\n")

    def write_summary(self, miss_count, summary):
        if not self.write_to_file:
            return
        summary.write(
            f"\nTotal miss count: {miss_count} out of {self.page_request_count} requests.\n")

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
        if self.write_to_file:
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
        if self.write_to_file:
            summary.close()
        return miss_count

    # use array of size self.cache_size, simiar to FIFO except add to front of list and move page number to front of list on cache hit
    # on cache miss with full cache, remove last element of list (least recent access) and insert new page to front
    def LRU(self):
        summary = self.get_output_handle("LRU")

        cache = []
        miss_count = 0

        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache:  # add to front, if needed remove last element
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size:  # cache full, remove last element
                    cache = cache[:-1]

                # add to front, push everything else back
                cache.insert(0, page)
            else:  # move page from current location to front
                cache.remove(page)
                cache.insert(0, page)

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        if self.write_to_file:
            summary.close()
        return miss_count

    # use 2 arrays of size self.cache_size, one for pages, one for markings, append new pages to back until full, then follow 1-bit lru
    def Rand_1Bit_LRU(self):
        summary = self.get_output_handle("Randomized_1Bit_LRU")

        cache = []
        markings = []  # bools: true = marked, false = unmarked
        miss_count = 0

        for i in range(self.page_request_count):
            page = self.requests[i]
            miss = False
            if page not in cache:  # if not full add to back, else replace random unmarked, else unmark all then replace random
                miss = True
                miss_count += 1
                unmarked = list()
                for a, b in enumerate(markings):
                    if(not b):
                        unmarked.append(a)

                if len(cache) < self.cache_size:  # just add to end of cache
                    cache.append(page)
                    markings.append(True)
                # at least one element of cache is unmarked, replace one random unmarked element
                elif(len(unmarked) > 0):
                    replace_ind = random.choice(unmarked)
                    cache[replace_ind] = page
                    markings[replace_ind] = True
                else:  # set all to unmarked then pick a random unmarked to replace
                    for a in range(len(markings)):
                        markings[a] = False
                    replace_ind = random.randint(0, len(cache)-1)
                    cache[replace_ind] = page
                    markings[replace_ind] = True
            else:  # cache hit, remark this page if needed
                ind = cache.index(page)
                markings[ind] = True

            self.write_action(miss, page, cache, summary)

        self.write_summary(miss_count, summary)
        if self.write_to_file:
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
            if (page_amount.get(page) != None):
                page_amount[page] += 1
            else:
                page_amount[page] = 1
            if page not in cache:
                miss = True
                miss_count += 1
                if len(cache) == self.cache_size:
                    lowestIndex = 0
                    for i in range(1, self.cache_size):
                        if page_amount[cache[i]] < page_amount[cache[lowestIndex]]:
                            lowestIndex = i

                    if page_amount[page] > page_amount[cache[lowestIndex]]:
                        cache[lowestIndex] = page

                else:
                    cache.append(page)

            self.write_action(miss, page, cache, summary)

        # for element in page_amount:
        #     print("page: " + str(element) + "  number: " + str(page_amount[element]))
        self.write_summary(miss_count, summary)
        if self.write_to_file:
            summary.close()
        return miss_count

    # LFD in O(NlogK) time, where N is the number of requests and K is the cache size
    def LFD(self):
        summary = self.get_output_handle("LFD")

        # Precalculate indices of each page
        occurrences = defaultdict(lambda: deque())
        for i in range(self.page_request_count):
            occurrences[self.requests[i]].append(i)

        def next_occurrence(page): return occurrences[page][0] if len(
            occurrences[page]) > 0 else float('inf')

        cache = set()
        prio_set = SortedSet()  # contains (next_occurrence, page)
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
        if self.write_to_file:
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
        if self.write_to_file:
            summary.close()
        return miss_count

    # adaptive cache replacement
    # adapted from https://www.usenix.org/legacy/events/fast03/tech/full_papers/megiddo/megiddo.pdf
    def ARC(self):
        p = 0
        t1, b1, t2, b2 = LRUList(), LRUList(
        ), LRUList(), LRUList()

        def replace(element):
            if t1.size() > 0 and (t1.size() > p or (b2.contains(element) and t1.size() == p)):
                b1.move_mru(t1.pop())
            else:
                b2.move_mru(t2.pop())

        summary = self.get_output_handle("ARC")
        miss_count = 0
        for page in self.requests:
            miss = False
            if t1.contains(page):
                t1.remove(page)
                t2.move_mru(page)
            elif t2.contains(page):
                t2.move_mru(page)
            else:
                miss = True
                miss_count += 1
                if b1.contains(page):
                    p = min(p + max(1, b2.size() / b1.size()), self.cache_size)
                    replace(page)
                    b1.remove(page)
                    t2.move_mru(page)
                elif b2.contains(page):
                    p = max(p - max(1, b1.size() / b2.size()), 0)
                    replace(page)
                    b2.remove(page)
                    t2.move_mru(page)
                else:
                    if t1.size() + b1.size() == self.cache_size:
                        if t1.size() < self.cache_size:
                            b1.pop()
                            replace(page)
                        else:
                            t1.pop()
                    elif t1.size() + b1.size() < self.cache_size:
                        total_size = t1.size() + t2.size() + b1.size() + b2.size()
                        if total_size >= self.cache_size:
                            if total_size == 2 * self.cache_size:
                                b2.pop()
                            replace(page)

                    t1.move_mru(page)

            self.write_action(
                miss, page, {**t1.get_cache(), **t2.get_cache()}.keys(), summary)
        self.write_summary(miss_count, summary)
        if self.write_to_file:
            summary.close()
        return miss_count

    def set_cache_size(self, cache_size):
        self.CACHE_SIZE = cache_size

    def set_request_page_count(self, page_request_count):
        self.PAGE_REQUESTS_COUNT = page_request_count



if __name__ == "__main__":
    mycache = cache(PAGE_NUM, PAGE_REQUEST_NUM, CACHE_SIZE)
    # mycache.generate_requests()
    rotation_request = []
    mycache.set_requests(generate_rotation_request(PAGE_NUM, PAGE_REQUEST_NUM))
    mycache.FIFO()
    mycache.LIFO()
    mycache.LFD()
    mycache.LFU()
    mycache.Random()
    mycache.LRU()
    mycache.Rand_1Bit_LRU()
    mycache.ARC()
