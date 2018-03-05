'''
Created on Feb 24, 2018
'''
import os
from collections import defaultdict
from feature import *

#parse the coreference fields of the file and obtain the mentions
def get_metions(tokens):
    
    mentions = []
    stack = defaultdict(list)

    # process from the last word of the sentence
    # check if this word is in a coref chain (the start)
    for i, t in reversed(list(enumerate(tokens))):
        if '(' not in t[-1]:
            continue
        ids = [int(x.replace(')','').replace('(','')) for x in t[-1].split('|') if x.startswith('(')]
        # j is actually the coref id of the chain
        # each coref id records the start word of all refexps in this chain that appear in the sentence
        for j in ids:
            stack[j].append((i,t))

    # process from the start word of the sentence
    # check if this word is in a coref chain (the end)
    for i, t in enumerate(tokens):
        if ')' not in t[-1]:
            continue
        ids = [int(x.replace(')','').replace('(','')) for x in t[-1].split('|') if x.endswith(')')]
        for j in ids:
            # s is the index of the start word of the refexp in this chain
            s = stack[j].pop()[0]
            mentions.append(Markable(tokens[s:i+1], (s,i), j))
       
    return mentions
       

# pair all extracted mentions with all possible combinations in one doc
# to create positive and negative train instances
def get_pairs(doc):
    pairs = []
    mentions = {}
    
    for sent_idx, sent in enumerate(doc):
        # each sentence gets a mention list
        mentions[sent_idx] = mention_list = get_metions(sent)
        
        #pair the in-sentence mentions
        for i in range(len(mention_list)-1,0,-1):
            anaphor = mention_list[i]
            for j in range(i-1,-1,-1):
                antecedent = mention_list[j]

                # pair all possible combinations between current refexp and every refexp before it
                # to see if they refer to the same referent
                if antecedent.end < anaphor.start:
                    pairs.append(MarkablePair(antecedent, anaphor, 1))
            
            # pair the in-document/cross-sentence mentions
            # check all sentences before current sentence, and all refexps in those
            # sentences must be antecedents
            for k in range(sent_idx-1,-1,-1):
                pairs.extend([MarkablePair(antecedent,anaphor,0) for antecedent in mentions[k]])
    
    return pairs
                   
        
#parse each raw file and extract features           
def build_features(path):
    X = []
    y = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith("auto_conll"):
                X_temp, y_temp = parse_file(os.path.join(root, file)) 
                X.extend(X_temp)
                y.extend(y_temp)

    return X, y
        
        
#helper function for parsing file     
def parse_file(path):
    doc = []
    sent = []
    corpus = []
    
    with open(path,'r', encoding="utf8") as f:
        for line in f:
            line = line.strip('\n')
            if not line:
                if sent:
                    doc.append(sent)
                    sent = []
                continue 
            
            if line.startswith('#begin'):
                doc = []
                sent = []
                continue
            elif line == '#end document':
                corpus.append(doc)
            else:
                fields = line.split()
                anns = [fields[2],fields[3],fields[4], fields[8],fields[10].strip('(*)'), fields[-1]]
                sent.append(anns)
                '''
                0    Word number    
                1    Word itself 
                2    Part-of-Speech    
                3    Word sense
                4    Named Entities
                5    Coreference
                '''
              
    X = [] # the refexp pairs in the whole corpus
    y = [] # the labels indicating if the pair refers to the same entity
    for doc in corpus:
        pairs = get_pairs(doc)
        # print(pairs)
        X.extend([p.feat for p in pairs])
        y.extend([p.label for p in pairs])
    
    return X, y

train_path = 'conll-2012/train/english/annotations'
build_features(train_path)