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
    
    for i, t in reversed(list(enumerate(tokens))):
        if '(' not in t[-1]:
            continue
        ids = [int(x.replace(')','').replace('(','')) for x in t[-1].split('|') if x.startswith('(')]
        for j in ids:
            stack[j].append((i,t))
    
    for i, t in enumerate(tokens):
        if ')' not in t[-1]:
            continue
        ids = [int(x.replace(')','').replace('(','')) for x in t[-1].split('|') if x.endswith(')')]
        for j in ids:
            s = stack[j].pop()[0]
            mentions.append(Markable(tokens[s:i+1], (s,i), j))
       
    return mentions
       

#pair the extracted mentions to create positive and negative train instances 
def get_pairs(doc):
    pairs = []
    mentions = {}
    
    for sent_idx, sent in enumerate(doc):
        mentions[sent_idx] = get_metions(sent)
        
        #pair the in-sentence mentions
        for i in range(len(mentions[sent_idx])-1,0,-1):
            anaphor = mentions[sent_idx][i]
            for j in range(i-1,-1,-1):
                antecedent = mentions[sent_idx][j]
                
                if antecedent.end < anaphor.start:
                    pairs.append(MarkablePair(antecedent, anaphor, 1))
            
            #pair the in-document/cross-sentence mentions
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
<<<<<<< HEAD
                anns = [fields[2],fields[3],fields[4], fields[8],fields[10].strip('(*)'), fields[-1]]
=======
                anns = [fields[2],fields[3],fields[4], fields[8],fields[10].strip('(*)'),fields[-1]]
>>>>>>> origin/master
                sent.append(anns)
                '''
                0    Word number    
                1    Word itself 
                2    Part-of-Speech    
                3    Word sense
                4    Named Entities
                5    Coreference
                '''
              
    X = []
    y = []
    for doc in corpus:
        pairs = get_pairs(doc)
        X.extend([p.feat for p in pairs])
        y.extend([p.label for p in pairs])
    
    return X, y

