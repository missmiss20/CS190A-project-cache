# CS190A-project
Final Project for UC Santa Barbara's CS190A Algorithm Course

Tianchen Wang
Winter 2022 CS 190A
Professor Suri

## cache.py
Contain a "cache" structure, the cache can use FIFO, LIFO, LRU, LFU, and the optimal offline strategy LFD
to process a series of page requests and record the miss rate to result.txt.
The cache size can be modified.

## query_generator.py
The query_generator.py uses the random library to generate a series of pseudo random page requests 
based on the total number of different pages.
