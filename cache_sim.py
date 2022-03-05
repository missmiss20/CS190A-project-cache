from collections import defaultdict, deque
from sortedcontainers import SortedSet
from llist import dllist
from lru_list import LRUList
import random


def arc(requests, capacity):
    p = 0
    t1 = LRUList()
    t2 = LRUList()
    b1 = LRUList()
    b2 = LRUList()
    misses = 0

    def replace(element):
        if t1.size() > 0 and (t1.size() > p or (b2.contains(element) and t1.size() == p)):
            b1.move_mru(t1.pop())
        else:
            b2.move_mru(t2.pop())

    for page in requests:
        if t1.contains(page):
            t1.remove(page)
            t2.move_mru(page)
        elif t2.contains(page):
            t2.move_mru(page)
        else:
            misses += 1
            if b1.contains(page):
                p = min(p + max(1, b2.size() / b1.size()), capacity)
                replace(page)
                b1.remove(page)
                t2.move_mru(page)
            elif b2.contains(page):
                p = max(p - max(1, b1.size() / b2.size()), 0)
                replace(page)
                b2.remove(page)
                t2.move_mru(page)
            else:
                if t1.size() + b1.size() == capacity:
                    if t1.size() < capacity:
                        b1.pop()
                        replace(page)
                    else:
                        t1.pop()
                elif t1.size() + b1.size() < capacity:
                    total_size = t1.size() + t2.size() + b1.size() + b2.size()
                    if total_size >= capacity:
                        if total_size == 2 * capacity:
                            b2.pop()
                        replace(page)
                t1.move_mru(page)

    return misses


def fifo(requests, capacity):
    cache = set()
    elements = deque()
    misses = 0

    for page in requests:
        if page not in cache:
            misses += 1
            if len(cache) == capacity:
                cache.remove(elements.popleft())
            elements.append(page)
            cache.add(page)

    return misses


def lfu(requests, capacity):
    nodes = {}
    freq = defaultdict(dllist)
    minfreq = 0
    size = 0
    misses = 0

    for page in requests:
        if page in nodes:
            node = nodes[page]
            frq = node.value[1]
            freq[frq].remove(node)
            if minfreq == frq and len(freq[frq]) == 0:
                minfreq += 1
            nodes[page] = freq[frq + 1].appendright([page, frq + 1])
        else:
            misses += 1
            if size == capacity:
                val = freq[minfreq].popleft()
                nodes.pop(val[0])
                size -= 1
            node = freq[1].appendright([page, 1])
            nodes[page] = node
            minfreq = 1
            size += 1

    return misses

def lru(requests, capacity):
    cache = LRUList()
    misses = 0

    for page in requests:
        if not cache.contains(page):
            misses += 1
            if cache.size() == capacity:
                cache.pop()
        cache.move_mru(page)

    return misses


def lifo(requests, capacity):
    cache = set()
    arr = []
    misses = 0

    for page in requests:
        if page not in cache:
            misses += 1
            if len(cache) == capacity:
                cache.remove(arr.pop())
            arr.append(page)
            cache.add(page)

    return misses


def rand(requests, capacity):
    cache = set()
    arr = []
    misses = 0

    for page in requests:
        if page not in cache:
            misses += 1
            if len(arr) == capacity:
                idx = random.randint(0, capacity - 1)
                cache.remove(arr[idx])
                arr[idx] = page
            else:
                arr.append(page)
            cache.add(page)

    return misses


def rand1bitlru(requests, capacity):
    cache = {}
    arr = []
    bitset = []
    misses = 0

    for page in requests:
        if page not in cache:
            misses += 1
            if len(cache) < capacity:
                cache[page] = len(arr)
                arr.append(page)
                bitset.append(1)
            else:
                unset = [i for i, b in enumerate(arr) if b == 0]
                if len(unset) > 0:
                    repl_idx = random.choice(unset)
                else:
                    bitset = [0] * len(bitset)
                    repl_idx = random.randint(0, len(arr) - 1)
                cache.pop(arr[repl_idx])
                arr[repl_idx] = page
                cache[page] = repl_idx
                bitset[repl_idx] = 1
        else:
            bitset[cache[page]] = 1 

    return misses

def lfd(requests, capacity):
    occurrences = defaultdict(lambda: deque())
    for i in range(len(requests)):
        occurrences[requests[i]].append(i)

    next_occurrence = lambda page : occurrences[page][0] if len(
        occurrences[page]) > 0 else float('inf')

    cache = set()
    prio_set = SortedSet()  # contains (next_occurrence, page)
    misses = 0
    for i in range(len(requests)):
        page = requests[i]
        occurrences[page].popleft()
        if page not in cache:
            misses += 1
            if len(cache) == capacity:
                cache.remove(prio_set.pop()[1])
            cache.add(page)
        else:
            prio_set.remove((i, page))
        prio_set.add((next_occurrence(page), page))

    return misses











   