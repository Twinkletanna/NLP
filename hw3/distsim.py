from __future__ import division
import operator
import sys,json,math
import os
import numpy as np
from numpy import linalg

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict
        

def calculate_cosine(a,b,word_to_ccdict):
    cosine, deno_a, deno_b=0,0,0
    dict_a=word_to_ccdict[a]
    dict_b=word_to_ccdict[b]
    for key in dict_a.keys():
        if key in dict_b.keys():
            cosine+=dict_a[key]*dict_b[key]
    for value in dict_a.values():
        deno_a+=value*value
    for value in dict_b.values():
        deno_b+=value*value
    return cosine/(math.sqrt(deno_a) *math.sqrt(deno_b))

def calculate_cosine2(a,b,word_to_ccdict):
    cosine, d1, d2=0,0,0
    cosine=np.dot(a,b)
    d1=np.linalg.norm(a)
    d2=np.linalg.norm(b)
    return cosine/(d1*d2)