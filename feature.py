'''
Created on Feb 24, 2018
'''

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
        f['named-entity'] = self.tokens[0][4]
        
        f['definite'] = self.is_definite()
        f['demonstrative'] = self.is_demos()
        f['pronoun'] = self.is_pronoun()
        
        return f
    
    
    def is_definite(self):
        if self.tokens[0][1].lower() == 'the':
            return 1
        
        return 0
        
        
    def is_demos(self):
        if self.tokens[0][1].lower() in ['this', 'that', 'these', 'those']:
            return 1
        
        return 0
        
        
    def sem_class(self,is_pronoun,NE):
        if is_pronoun:
            word = self.tokens[0][1].lower()
            if word in {'he','she','you','i','me','her','him','his','hers','mine','us','ours','we'}:
                return 1
            if word in {'it','its'}:
                return 0
            if word in {'them','they','their'}:
                return 2
        else:
            if NE in {'NORP','PERSON'}:
                return 1
            if NE in {'TIME','GPE','ORG','CARDINAL','LOC','QUANTITY','DATE','FAC'}:
                return 0
            else:
                return 2
        return 2
        
        
    def is_pronoun(self):
        if len(self.tokens) == 1:
            if self.tokens[0][2].startswith('PRP'):
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
        
        f['antecedent_text'] = self.antecedent['text']
        f['antecedent_NE'] = self.antecedent['named-entity']
        f['antecedent_definite'] = self.antecedent['definite']
        f['antecedent_demonstrative'] = self.antecedent['demonstrative']
        f['antecedent_pronoun'] = self.antecedent['pronoun']
      
        f['anaphor_text'] = self.anaphor['text']
        f['anaphor_NE'] = self.anaphor['named-entity']
        f['anaphor_definite'] = self.anaphor['definite']
        f['anaphor_demonstrative'] = self.anaphor['demonstrative']
        f['anaphor_pronoun'] = self.anaphor['pronoun']
        
        return f    

