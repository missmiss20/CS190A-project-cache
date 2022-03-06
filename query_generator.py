from mimetypes import init
import numpy as np
import random
# there are "page_num" distinct pages
PAGE_NUM = 100
# our query requests "query_length" pages
QUERY_LENGTH = 100

# generate #query_length page requests with a normal distribution
def generate_normal_distribution(page_num, query_length):
    output = []
    i = 0
    # generate almost mornal distribution
    while i < query_length:
        x = np.random.normal(page_num/2, page_num/6, 1)
        x = int(x)
        # this function has a 0.02% chance to produce a out of bound page number, 
        # wich will be discarded.
        if x < 1 or x > page_num:
            i-=1
        else:
            output.append(x)
        i+=1

    return output

# generate #query_length page requests with a triangular distribution
# triangle begin from 'left', end at 'page_num+1', with height at 'mode'
def generate_triangular_distribution(page_num, query_length, left=1, mode=1):
    output = []
    i = 0
    while i < query_length:
        x = int(np.random.triangular(left, mode, page_num+1))
        output.append(x)
        i+=1

    return output

# generate #query_length page requests with fix radios
# 'radios' contains the radio of the appreaence frequency of all pages
# Ex: 5 pages, with radios = [4,2,2,1,1], the page 1 will apprear 4 time as frequent as page 4 and 5

def generate_ratio_distribution(page_num: int, query_length: int, radios: list()):
    if page_num != len(radios):
        print("Error, page_num not equal to len of radios\n")
        return []

    draw_bag = []
    for i in range(len(radios)):
        for j in range(radios[i]):
            draw_bag.append(i+1)

    length = len(draw_bag)
    # print(draw_bag)
    requests = []
    for _ in range(query_length):
        draw = np.random.randint(0, length-1)
        requests.append(draw_bag[draw])
    
    return requests

def generate_rotation_request(PAGE_NUM, PAGE_REQUEST_NUM):
    rotation_request = []
    for i in range(1, PAGE_REQUEST_NUM+1):
        if i % PAGE_NUM != 0:
            rotation_request.append(i % PAGE_NUM)
        else:
            rotation_request.append(PAGE_NUM)
    return rotation_request


# The Long Tail is an example of a Power Law probability distribution, such as the Pareto distribution or 80:20 rule. 
# If 20% of objects are used 80% of the time and a way can be found to reduce the cost of obtaining that 20%, 
# system performance will improve.
def pareto_distribution(page_num: int, query_length: int):
    
    eighty_percent_mark = page_num / 5

    requests = []
    for _ in range(query_length):
        eighty_twenty = random.randint(1, 5)
        if eighty_twenty == 5:
            draw = np.random.randint(eighty_percent_mark+1, page_num)
        else:
            draw = np.random.randint(1, eighty_percent_mark)
        
        requests.append(draw)

    return requests

if __name__ == "__main__":
    page_num = 102
    query_length = 100000

    # tests to validate generated page requests 

    # output = generate_normal_distribution(page_num, query_length)
    # file = open("a.txt","w")
    # file.write(str(output))

    # output = generate_triangular_distribution(page_num, query_length)
    # file = open("a.txt","w")
    # file.write(str(output))

    # frequency_radio = [4,2,2,1,1]
    # output = generate_ratio_distribution(5, 20, frequency_radio)
    # file = open("a.txt","w")
    # file.write(str(output))

    # output = pareto_distribution(page_num, query_length)
    # count1 = 0
    # count58 = 0
    # for i in output:
    #     if i <= 20:
    #         count1 += 1
    #     else:
    #         count58 += 1
    
    # print(count1)
    # print(count58)