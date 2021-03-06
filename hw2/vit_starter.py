from __future__ import division
import numpy as np

def dict_argmax(dct):
    """Return the key whose value is largest. In other words: argmax_k dct[k].
    Behavior undefined if ties (python docs might give clues)"""
    return max(dct.iterkeys(), key=lambda k: dct[k])

def goodness_score(seq, A_factor, B_factors):
    # the total "goodness" score of the proposed sequence
    N = len(B_factors)
    score = 0
    score += sum(A_factor[seq[t],seq[t+1]] for t in range(N-1))
    score += sum(B_factors[t][seq[t]] for t in range(N))
    return score

def exhaustive(A_factor, B_factors, output_vocab):
    # the exhaustive decoding algorithm.
    N = len(B_factors)  # length of entire sentence

    def allpaths(sofar):
        # Recursively generate all sequences given a prefix "sofar".
        # this probably could be redone cleverly as a python generator
        retpaths = []
        if len(sofar)==N:
            return [sofar]
        for sym in output_vocab:
            newpath = sofar[:] + [sym]
            retpaths += allpaths(newpath)
        return retpaths

    path_scores = {}
    for path in allpaths([]):
        path = tuple(path)  # tuple version can be used as dict key
        score = goodness_score(path, A_factor, B_factors)
        path_scores[path] = score
    bestseq = dict_argmax(path_scores)
    return list(bestseq)  # might as well convert it to a list, why not

def viterbi(A_factor, B_factors, output_vocab):
    """
    A_factor: a dict of key:value pairs of the form
        {(curtag,nexttag): score}
    with keys for all K^2 possible neighboring combinations,
    and scores are numbers.  We assume they should be used ADDITIVELY, i.e. in log space.
    higher scores mean MORE PREFERRED by the model.

    B_factors: a list where each entry is a dict {tag:score}, so like
    [ {Noun:-1.2, Adj:-3.4}, {Noun:-0.2, Adj:-7.1}, .... ]
    each entry in the list corresponds to each position in the input.

    output_vocab: a set of strings, which is the vocabulary of possible output
    symbols.

    RETURNS:
    the tag sequence yvec with the highest goodness score
    """
    

    N = len(B_factors)   # length of input sentence
    # viterbi log-prob tables
    V = [{tag:0 for tag in output_vocab} for t in range(N)]
    # backpointer tables
    # back[0] could be left empty. it will never be used.
    back = [{tag:None for tag in output_vocab} for t in range(N)]
    # todo implement the main viterbi loop here
    # you may want to handle the t=0 case separately
    for t in range(N):
        for tag in output_vocab:
            if t==0:
                V[t][tag]=B_factors[t][tag]
            else:
                maxi=0
                sel_j=tag
                for j in output_vocab:
                    temp=(V[t-1][j]+A_factor[(j,tag)]+B_factors[t][tag])
                    if temp>maxi:
                        maxi=temp
                        sel_j=j
                V[t][tag]=maxi                
                back[t][tag]=sel_j
        
    path=[dict_argmax(V[-1])]
    output_vocab=list(output_vocab)
    for i in range(N-1,0,-1):
        path.append(back[i][path[-1]])
    pathrev=path[::-1]
    return pathrev

def randomized_test(N=3, V=5):
    # This creates a random model and checks if the exhaustive and viterbi
    # decoders agree.
    import random
    A = { (a,b): random.random() for a in range(V) for b in range(V) }
    Bs = [ [random.random() for k in range(V)] for i in range(N)]

    print "output_vocab= ", range(V)
    print "A=", A
    print "Bs=",Bs


    fromex  = exhaustive(A,Bs, range(V))
    fromvit = viterbi(A,Bs,range(V))
    print fromex
    print fromvit
    assert fromex==fromvit
    print "Worked!"

if __name__=='__main__':
    A = {(0,0):3, (0,1):0, (1,0):0, (1,1):3}
    Bs= [ [0,1], [0,1], [30,0] ]
    # that's equivalent to: [ {0:0,1:1}, {0:0,1:1}, {0:30,1:0} ]

    y = exhaustive(A, Bs, set([0,1]))
    print "Exhaustive decoding:", y
    print "score:", goodness_score(y, A, Bs)
    y = viterbi(A, Bs, set([0,1]))
    print "Viterbi    decoding:", y
    randomized_test()