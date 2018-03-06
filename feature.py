'''
Created on Feb 24, 2018
'''
from nltk.corpus import wordnet as wn

class Markable(object):
    def __init__(self, tokens, span, label):
        self.tokens = tokens
        self.start = span[0]
        self.end = span[1]
        
        self.label = label
        self.feat = self.features()

    def features(self):
        f = {}
        
        f['text'] = ' '.join([t[1] for t in self.tokens])
        f['named-entity'] = self.tokens[0][4] if self.tokens[0][4] != '' else 'OTHER'
        
        f['definite'] = self.is_definite()
        f['demonstrative'] = self.is_demos()
        f['pronoun'] = self.is_pronoun()
        f['proper_noun'] = self.is_proper_noun()
        f['number'] = self.get_number()
        
        #print(f)
        return f
    
    
    def get_number(self):
        single=['he','his','she','her','i','my','it','its']
        plural=['they','their','our','us']
        
        if self.tokens[0][1] in single:
            return 1
        if self.tokens[0][1] in plural:
            return 2
        
        return 0
    
    
    def is_proper_noun(self):
        for word in self.tokens:
            if word[2] in ['NNP', 'NNPS']:
                return 1
        
        return 0
        
        
    def is_definite(self):
        if self.tokens[0][1].lower() == 'the':
            return 1
        
        return 0
        
        
    def is_demos(self):
        if self.tokens[0][1].lower() in ['this', 'that', 'these', 'those']:
            return 1
        
        return 0
           
        
    def is_pronoun(self):
        if len(self.tokens) == 1:
            if self.tokens[0][2] in ['PRP', 'PRP$']:
                return 1
        return 0
    
    
class MarkablePair(object):

    def __init__(self, antecedent, anaphor, same_sent):
        self.antecedent = antecedent.feat
        self.anaphor = anaphor.feat
        self.label = True if antecedent.label == anaphor.label else False
        
        self.same_sentence = same_sent
        self.feat = self.features()
        
        
    def features(self):
        f = {}
        f['in_sentences'] = self.same_sentence
        
        f['antecedent_definite'] = self.antecedent['definite']
        f['antecedent_demonstrative'] = self.antecedent['demonstrative']
        f['antecedent_pronoun'] = self.antecedent['pronoun']
        f['antecedent_proper_noun'] = self.antecedent['proper_noun']
        
        f['anaphor_definite'] = self.anaphor['definite']
        f['anaphor_demonstrative'] = self.anaphor['demonstrative']
        f['anaphor_pronoun'] = self.anaphor['pronoun']
        f['anaphor_proper_noun'] = self.anaphor['proper_noun']
        
        #The last word of antecedent and anaphor match or not
        f['last_word_match'] = 1 if self.antecedent['text'].split()[-1] == self.anaphor['text'].split()[-1] else 0
        
        #Whether antecedent and anaphor are exactly the same in String
        f['string_match'] = 1 if self.antecedent['text'] == self.anaphor['text'] else 0
        
        #Same entity type
        f['ner_match'] = 1 if self.antecedent['named-entity'] == self.anaphor['named-entity'] else 0
        
        #number match
        f['number_match'] = self.number_match()
        
        #Substring
        f['substring'] = self.is_substring()
        return f
    
    
    def is_substring(self):
        f1 = self.antecedent['text']
        f2 = self.anaphor['text']
        
        if f1 in f2 or f2 in f1:
            return 1
        return 0
        
        
    def number_match(self):
        f1 = self.antecedent['number']
        f2 = self.anaphor['number']
        
        if f1 == 2 or f2 == 2: 
            return 2
        if f1 == f2: 
            return 1
        
        return 0
        
    
    def is_hyponyms(self):
        
        f1 = self.antecedent['text']
        f2 = self.self.anaphor['text']
        
        return f2 in f1.hyponyms() or f1 in f2.hyponyms()
