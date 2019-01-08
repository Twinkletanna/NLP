from pprint import pprint

# The productions rules have to be binarized.

grammar_text = """
S -> NP VP
S -> NPP VP
S -> NP VPP
S -> NPP VPS
NP -> Det Noun
NPP -> Det Nounp
VP -> Verb NP
VPP -> Verbp NP
VPS -> Verbs NP
PP -> Prep NP
NP -> NP PP
VP -> VP PP
"""

lexicon = {
    'Noun': set(['cat', 'dog', 'table', 'food','attack']),
    'Nounp':set(['dogs','cats']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated']),
    'Verbp':set(['attacks']),
    'Verbs':set(['attack']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
}

# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)
possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

#print "Grammar rules in tuple form:"
#pprint(grammar_rules)
#print "Rule parents indexed by children:"
#pprint(possible_parents_for_children)


def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon

    # Set up the cells data structure.
    # It is intended that the cell indexed by (i,j)
    # refers to the span, in python notation, sentence[i:j],
    # which is start-inclusive, end-exclusive, which means it includes tokens
    # at indexes i, i+1, ... j-1.
    # So sentence[3:4] is the 3rd word, and sentence[3:6] is a 3-length phrase,
    # at indexes 3, 4, and 5.
    # Each cell would then contain a list of possible nonterminal symbols for that span.
    # If you want, feel free to use a totally different data structure.
    N = len(sentence)
    cells = {}
    for i in range(N+1):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    # TODO replace the below with an implementation
    
    for i in range(N+1):
       for j in range(0, N -i+1):
           if i==1:
               for pos in lexicon.keys():
                   if sentence[j:j+i][0] in lexicon[pos]:
                       cells[(j,j+i)].append(pos)     
           for k in range(j+1,j+i):
               end=j+i
               if i!=1:
                   for B in cells[(j,k)]:
                       for C in cells[(k,end)]:
                           if  (B,C) in possible_parents_for_children:
                               cells[(j, end)] = possible_parents_for_children[(B,C)]     
    flag=False
    for k in cells.values():
        if 'S' in k:
            flag=True
    return flag


def cky_parse(sentence):
    # Return one of the legal parses for the sentence.
    # If nothing is legal, return None.
    # This will be similar to cky_acceptance(), except with backpointers.
    global grammar_rules, lexicon

    N = len(sentence)
    cells = {}
    parse = {}
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
           for k in range(j+1,j+i):
               end=j+i
               if i!=1:
                   for B in cells[(j,k)]:
                       for C in cells[(k,end)]:
                           if  (B,C) in possible_parents_for_children:
                               cells[(j, end)] = possible_parents_for_children[(B,C)]     
                               parse[(j,j+i)] =   [possible_parents_for_children[(B,C)][0],[parse[j,k],parse[k,end]  ]]
    

    flag=None
    for k,v in cells.iteritems():
        if 'S' in v:
            if flag==None:
				flag=[]
            flag.append(parse[k])
                               
    return flag

## some examples of calling these things...
## you probably want to call only one sentence at a time to help debug more easily.

#print cky_acceptance(['the','cat','attacked','the','food'])
#pprint( cky_parse(['the','cat','attacked','the','food']))
#pprint( cky_acceptance(['the','the']))
#pprint( cky_parse(['the','the']))
#print cky_acceptance(['the','cat','attacked','the','food','with','a','dog'])
#pprint( cky_parse(['the','cat','attacked','the','food','with','a','dog']) )
#pprint( cky_acceptance(['the','cat','with','a','table','attacked','the','food']) )
#pprint( cky_parse(['the','cat','with','a','table','attacked','the','food']) )
