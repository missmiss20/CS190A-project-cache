from mimetypes import init
import numpy as np

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

def generate_triangular_distribution(page_num, query_length, left=1, mode=1):
    output = []
    i = 0
    while i < query_length:
        x = int(np.random.triangular(left, mode, page_num+1))
        output.append(x)
        i+=1

    return output

def generate_ratio_distribution(page_num: int, query_length: int, frequency_radio: list[int]):
    if page_num != len(frequency_radio):
        print("Error")
        return []

    draw_bag = []
    for i in range(len(frequency_radio)):
        for j in range(frequency_radio[i]):
            draw_bag.append(i+1)

    length = len(draw_bag)
    print(draw_bag)
    requests = []
    for _ in range(query_length):
        draw = np.random.randint(0, length-1)
        requests.append(draw_bag[draw])
    
    return requests


if __name__ == "__main__":
    page_num = 100
    query_length = 100000
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
