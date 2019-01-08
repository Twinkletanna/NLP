from pprint import pprint
from collections import defaultdict


grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}


def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO Fill in your implementation for processing the grammar rules.
    with open('pcfg_grammar_modified','r') as g_file:
        for line in g_file:
            left,right=line.split("->")
            left=left.strip()
            rightside=right.split()
            if len(rightside)>2:
                key=(left,rightside[0],rightside[1])
                rule=(left,tuple(rightside[:-1]))
                grammar_rules.append(rule)
            elif len(rightside)==2:
                key=(left,rightside[0])
                rule=(left,rightside[:-1][0] )
                if left not in lexicon:
                    lexicon[left]=set([])
                lexicon[left].add(rule[1])
                
            if key not in probabilities:
                probabilities[key]=float(rightside[-1])
            
            
    all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
    for par, (left,right) in grammar_rules:
        if left not in all_parents or right not in all_parents:
            assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." 

    possible_parents_for_children = {}
    for parent, (left,right) in grammar_rules:
        if  (left,right) not in possible_parents_for_children:
            possible_parents_for_children[left, right] = []
        possible_parents_for_children[left, right].append(parent)
     
    pass
    print "Grammar rules in tuple form:"
    pprint(grammar_rules)
    print "Rule parents indexed by children:"
    pprint(possible_parents_for_children)
    print "probabilities"
    pprint(probabilities)
    print "Lexicon"
    pprint(lexicon)


def pcky_parse(sentence):
    # Return the most probable legal parse for the sentence
    # If nothing is legal, return None.
    # This will be similar to cky_parse(), except with probabilities.
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    # TODO complete the implementation
    
    N = len(sentence)
    cells = {}
    parse = {}
    table=defaultdict(float)
    back=defaultdict()
    prob={}
    for i in range(N+1):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    for i in range(N+1):
       for j in range(0, N -i+1):
           if i==1:
               for pos in lexicon.keys():
                   if sentence[j:j+i][0] in lexicon[pos]:
                       cells[(j,j+i)].append(pos)     
                       parse[(j,j+i)]=[pos,sentence[j:j+i][0]]
                       prob[(j,j+i)]=probabilities[(pos,sentence[j:j+i][0])]
                       table[(j,j+i,pos)]=probabilities[(pos,sentence[j:j+i][0])]
           for k in range(j+1,j+i):
               end=j+i
               if 1:
                   for B in cells[(j,k)]:
                       for C in cells[(k,end)]:
                           if  (B,C) in possible_parents_for_children and table[j,k,B]>0 and table[k,end,C]>0:
                               parent=possible_parents_for_children[(B,C)]
                               cells[(j, end)] = parent
                               for p in parent:
                                   if(table[j,end,p]<probabilities[p,B,C]*table[j,k,B]*table[k,end,C]  ):
                                       table[j,end,p]=probabilities[p,B,C]*table[j,k,B]*table[k,end,C]
                                       back[j,end,p]=(k,B,C)
                                       

    print ("\n")
    flag=False
    for k in table.keys():
		if k==(0,N,'S') :
			print getpath2(0,N,'S',sentence,back)
			print table[k]
			flag=True
    
    return flag

        
def getpath2(i,j,part,sentence,back):
    if j==i:
        return
    if j-i==1:
       return [part,sentence[i:j][0]]
    else:
        (s,p1,p2)=back[i,j,part] 
        return [part,[getpath2(i,s,p1,sentence,back),getpath2(s,j,p2,sentence,back)]] 
	
	
    
    