from cache import *

WELCOME = "CS190A Project\nJerry Wang, Brian Qiu, Erwan Fraisse, Rhys Tracy\nTopic 2, Caching Methods.\n"
ENTER_CACHING_METHOD = """
Please Select Caching Method: \n
     First In First Out, FIFO: 1\n
      Last In First Out, LIFO: 2\n
Longest Forward Distance, LFD: 3\n
   Least Frequently Used, LFU: 4\n
                       Random: 5\n
     Least Recently Used, LFU: 6\n
                        Exit: -1\n
"""

ENTER_INFO = """
Usage: page_number page_request_count cache_size\n
Example: 10 50 5\n
"""
SIMULATING = "Simulation in progress\n"
OUTPUT_SUMMARY = "Output Summary:\n"

def interface():
    print(WELCOME)
    while(1):
        method = input(ENTER_CACHING_METHOD)
        if type(method)!= int or method > 6 or method == 0:
            print("Invalid Input.")
        elif method < 0:
            break
        else:
            

    print("Bye")
    return 0


if __name__ == "__main__":

    mycache = cache(PAGE_NUM, PAGE_REQUEST_NUM, CACHE_SIZE)
    mycache.generate_requests()
    mycache.FIFO()
    mycache.LIFO()
    mycache.LFD()