'''
Created on Feb 24, 2018
'''

# a refexp instance in a sentence
class Markable(object):
    def __init__(self, tokens, span, label):
        # tokens are the segment of refexp
        self.tokens = tokens
        # start and end in span are inclusive
        self.start = span[0]
        self.end = span[1]

        # coref chain id of this refexp
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
        
        #print(f)
        return f
    
    
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
    
# a pair of refexps from a doc to indicate if they refer to the same chain id/entity
class MarkablePair(object):

    def __init__(self, antecedent: Markable, anaphor: Markable, same_sent: int):
        self.antecedent = antecedent.feat
        self.anaphor = anaphor.feat
        # check if two refexp belong to the same chain id
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
        f['antecedent_proper_noun'] = self.antecedent['proper_noun']
        
        f['anaphor_text'] = self.anaphor['text']
        f['anaphor_NE'] = self.anaphor['named-entity']
        f['anaphor_definite'] = self.anaphor['definite']
        f['anaphor_demonstrative'] = self.anaphor['demonstrative']
        f['anaphor_pronoun'] = self.anaphor['pronoun']
        f['anaphor_proper_noun'] = self.anaphor['proper_noun']
        
        return f

