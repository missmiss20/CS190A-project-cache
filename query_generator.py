from mimetypes import init
from time import clock_gettime
import random

# there are "page_num" distinct pages
PAGE_NUM = 100
# our query requests "query_length" pages
QUERY_LENGTH = 100

def generate(page_num, query_length):
    output = []
    for i in range(query_length):
        output.append(random.randint(1, page_num))

    return output

if __name__ == "__main__":
    query = generate(PAGE_NUM, QUERY_LENGTH)
    print(query)