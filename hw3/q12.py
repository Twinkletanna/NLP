import  math
#import nltk
import operator
from collections import defaultdict
from sets import Set

pos_seedlist=["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
neg_seedlist=["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]

sentences=open('/home/twinkle/NLP/hw3/tweets.txt').read().strip().split("\n")
#one row
#condition to ignore
wordcounts=defaultdict(int)
pair_counts=defaultdict(int)
seedsum=defaultdict(float)
pmi=defaultdict(float)
polarity=defaultdict(float)
total=0
bow=Set()
words=[]
allwords=[]
#make a set, wordsum, break loop for both, 
i=0
i=0
#bla=[]
for sent in sentences:
    print i
    
    i+=1
    temp=sent.split(' ')
    words+=temp
    setwords=Set(temp)
    bow=bow|setwords
#    words=sent.split(' ')
#    allwords+=words
    for word in setwords:
        word=word.lower()
        wordcounts[word]+=1
        condition=(word in pos_seedlist) or (word in neg_seedlist) or (word[0]=='@') or (word[0]=='#')  or (word[:5]=='https') or (word=='RT') or (word==':')
        if not condition:
            for seed in pos_seedlist:
                if sent.find(seed) != -1 :
                    pair_counts[(word,'pos')]+=1
                    seedsum['pos']+=pair_counts[(word,'pos')]
            for seed in neg_seedlist:
                if sent.find(seed) != -1 :
                    pair_counts[(word,'neg')]+=1
                    seedsum['neg']+=pair_counts[(word,'pos')]
total=seedsum['pos']+seedsum['neg']

print "DONE PAIR_COUNTS"
for key in pair_counts.keys():
    den=seedsum[key[1]]*wordcounts[key[0]]+len(pair_counts)
    if den==0:
        print seedsum[key[1]], wordcounts[key[0]],key
    pmi=(total*pair_counts[key]+1)/den
#    ppmi[key]=max(math.log(pmi),0)
print "DONE PMI"

#polarity
for key in pair_counts.keys():
    polarity[key[0]]=pmi[(key[0],'pos')]-pmi[(key[0],'neg')]
    
print polarity
print"\n\n\n"
    
sorted_polarity1=sorted(polarity.items(),key=operator.itemgetter(1))
sorted_polarity2=sorted(polarity.items(),key=operator.itemgetter(1),reverse=True)
print "ACCENDING",sorted_polarity1[:20]
print "REVERSE",sorted_polarity2[:20]