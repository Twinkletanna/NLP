#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 18:14:12 2017

@author: twinkle
"""
from collections import defaultdict
import math
words=defaultdict()

worddata=open('/home/twinkle/NLP/hw3/nytcounts.university_cat_dog').read().split('\n')
for part in worddata:
    words[part.split('\t')[0]]=part.split('\t')

def calculate_cosine(a,b):
    cosine=0
    dict_a=words[a][2]
    dict_b=words[b][2]
    for key in dict_a.keys():
        if key in dict_b.keys():
            cosine+=dict_a[key]*dict_b[key]
    return cosine