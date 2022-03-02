from pickle import TRUE
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
          iteration_compare(): 7
                        Exit: -1
"""
ENTER_CACHING_METHOD_ERROR = """
Bad input! Please enter a valid number
"""
ENTER_INFO = """
Please enter page number, total number of page requests, and cache size
"""
ENTER_INFO_ERROR = """
Bad input! Please enter 3 integers
Sample Usage: 10 50 5
Resulting in page_number = 10 page_request_count = 50 cache_size = 5
"""

ENTER_REQUEST_TYPE = """
Please Enter Page Request Type:
                     Random: 0
        normal distribution: 1
      triangle distribution: 2
             arbitary radio: 3
"""

SIMULATING = "Simulation in progress\n"
OUTPUT_SUMMARY = "Output Available\n"

NORMAL_DISTRIBUTION = 1
TRIANGLE_DISTRIBUTION = 2
ARBITARY_RADIO_DISTRIBUTION = 3
WRITE_TO_FILE = False

def interface():
    print(WELCOME)
    while(1):
        try:
            method = int(input(ENTER_CACHING_METHOD))
        except:
            print(ENTER_CACHING_METHOD_ERROR)
            continue
        if method == 7:
            iteration_compare()
            continue
        elif method > 6 or method == 0:
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

                mycache = cache(page_num, page_request_num, cache_size, WRITE_TO_FILE)
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


def iteration_compare():
    while(1):
        try:
            it_count = int(input("Enter number of iterations or -1 to exit iteration_compare\n"))
            if it_count < 0:
                return 0
        except:
            print("Please enter a valid number\n")
            continue

        while(1):
            try:
                a_list = list(map(int, input(ENTER_INFO).split()))
                if len(a_list) != 3 :
                    print(ENTER_INFO_ERROR)
                    continue
            except:
                print(ENTER_INFO_ERROR)
                continue
            break

        while(1):
            try:
                request_type = int(input(ENTER_REQUEST_TYPE))
                if request_type > 3 or request_type < 0:
                    print("Please enter a valid number\n")
                    continue
            except:
                print("Bad Input\n")
                continue

            break


        page_num, page_request_num, cache_size = a_list

        FIFO_miss = 0
        LIFO_miss = 0
        LFD_miss = 0
        LFU_miss = 0
        Random_miss = 0
        LRU_miss = 0
        Rand_1Bit_LRU_miss = 0
        ARC_miss = 0

        total_requests = it_count * page_request_num
        if total_requests > 10**6:
            print("Try a smaller number\n")
            continue

        ratios = []
        if request_type == 3:
            while(1):
                ratios = list(map(int, input("Enter occurrence radio for each page:\n").split()))
                if len(ratios) != page_num:
                    print("Error! Need %d numbers" % page_num)
                    continue
                break

        for i in range(it_count):
            mycache = cache(page_num, page_request_num, cache_size, WRITE_TO_FILE)
            mycache.generate_requests(request_type, ratios)

            FIFO_miss += mycache.FIFO()
            LIFO_miss += mycache.LIFO()
            LFD_miss += mycache.LFD()
            LFU_miss += mycache.LFU()
            Random_miss += mycache.Random()
            LRU_miss += mycache.LRU()
            Rand_1Bit_LRU_miss += mycache.Rand_1Bit_LRU()
            ARC_miss += mycache.ARC()

        summary = """In a total of {0} requests, 
        FIFO has {1} misses, with a miss rate of {2:.4f}
        LIFO has {3} misses, with a miss rate of {4:.4f}
        LFD has {5} misses, with a miss rate of {6:.4f}
        LFU has {7} misses, with a miss rate of {8:.4f}
        Random has {9} misses, with a miss rate of {10:.4f}
        LRU has {11} misses, with a miss rate of {12:.4f}
        Rand_1Bit_LRU has {13} misses, with a miss rate of {14:.4f}
        ARC has {15} misses, with a miss rate of {16:.4f}
        """.format(total_requests, FIFO_miss, FIFO_miss/total_requests,
                                LIFO_miss, LIFO_miss/total_requests,
                                LFD_miss, LFD_miss/total_requests,
                                LFU_miss, LFU_miss/total_requests,
                                Random_miss, Random_miss/total_requests,
                                LRU_miss, LRU_miss/total_requests,
                                Rand_1Bit_LRU_miss, Rand_1Bit_LRU_miss/total_requests,
                                ARC_miss, ARC_miss/total_requests,
                                )

        print(summary)

    return 0

if __name__ == "__main__":
    interface()