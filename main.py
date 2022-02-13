from cache import *

WELCOME = "CS190A Project\nJerry Wang, Brian Qiu, Erwan Fraisse, Rhys Tracy\nTopic 2, Caching Methods.\n"
ENTER_CACHING_METHOD = """
New Simulation:
Please Select Caching Method:
     First In First Out, FIFO: 1
      Last In First Out, LIFO: 2
Longest Forward Distance, LFD: 3
   Least Frequently Used, LFU: 4
                       Random: 5
     Least Recently Used, LFU: 6
                        Exit: -1
"""
ENTER_CACHING_METHOD_ERROR = """
Bad input! Please enter a valid number
"""
ENTER_INFO = """
Please enter page number, total number Of page requests, and cache size
"""
ENTER_INFO_ERROR = """
Bad input! Please enter 3 integers
Sample Usage: 10 50 5
Resulting in page_number = 10 page_request_count = 50 cache_size = 5
"""


SIMULATING = "Simulation in progress\n"
OUTPUT_SUMMARY = "Output Available\n"

def interface():
    print(WELCOME)
    while(1):
        try:
            method = int(input(ENTER_CACHING_METHOD))
        except:
            print(ENTER_CACHING_METHOD_ERROR)
            continue
        if method > 6 or method == 0:
            print(ENTER_CACHING_METHOD_ERROR)
            continue
        elif method < 0:
            break
        else:
            while(1):
                try:
                    a_list = list(map(int, input(ENTER_INFO).split()))
                    if len(a_list) != 3 :
                        print(ENTER_INFO_ERROR)
                        continue
                except:
                    print(ENTER_INFO_ERROR)
                    continue

                print(SIMULATING)
                page_num, page_request_num, cache_size = a_list

                mycache = cache(page_num, page_request_num, cache_size)
                mycache.generate_requests()

                if method == 1:
                    mycache.FIFO()
                elif method == 2:
                    mycache.LIFO()
                elif method == 3:
                    mycache.LFD()
                elif method == 4:
                    mycache.LFU()
                elif method == 5:
                    mycache.Random()
                elif method == 6:
                    mycache.LRU()
                
                # can continue with print out output summary
                print(OUTPUT_SUMMARY)
                break

    print("Bye")
    return 0


if __name__ == "__main__":
    interface()