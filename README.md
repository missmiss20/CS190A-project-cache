# CS190A-project
Final Project for UC Santa Barbara's CS190A Algorithm Course



Tianchen Wang
Winter 2022 CS 190A
Professor Suri

The Performance Analysis of Different Cache Policies Under Diverse Page Request and Operating Scenarios

This project explores the miss rate of different caching policies such as FIFO, LIFO, LRU, LFU and validates the miss rate of the optimal offline caching algorithm LFD by designing and creating caching and page request generation programs. Furthermore, this project will analyze each method's space complexity and potential running time.

The page request generation program will generate an array of page requests ready to be fed into the caching programs. It should create page requests with a changeable number of distinct pages and different lengths, the dictionary of all pages(main memory), and pages with entirely random frequencies, a normal distribution, or other kinds of distributions.

The caching program will take the output of the page request generation program as input page requests. It will allow testers to use FIFO, LIFO, LRU, LFU caching policies to process the requests. And it will output the running time, space used, miss page count, and miss page comparison with the optimal offline caching algorithm LFD.

After these programs are built, it is possible to expand the research program. It is possible to explore the scenario of parallel computing of caches. (1). When the cache is divided into n equally sized sub-caches, process the page request simultaneously. (2). When multiple processes share the same cache. How will the efficiency of LRU change in these scenarios?

During weeks three to five, the first part of the project will be finished with a minimum variable product of a page request generation program and cache program. From weeks six to eight, the project will dip in multi-processing. By week nine, the project should be finished and ready to present.