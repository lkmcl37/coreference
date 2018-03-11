class Markable(object):
    def __init__(self, tokens, span, label, doc_id, part_id, sent_id):
        self.tokens = tokens  # tokens are the segment of refexp
        self.span = span      # start and end in span are inclusive
        self.feat = self.features()

        self.label = label    # coref chain id of this refexp
        self.position = (doc_id, part_id, sent_id)
        

    def features(self):
        f = {}

        f['text'] = ' '.join([t[3] for t in self.tokens])
        ne = self.tokens[0][10].strip("(*)")
        f['named-entity'] = ne if ne != '' else 'OTHER'

        f['definite'] = self.is_definite()
        f['demonstrative'] = self.is_demos()
        f['pronoun'] = self.is_pronoun()
        f['proper_noun'] = self.is_proper_noun()
        f['number'] = self.get_number()
        f['sem'] = self.get_sem()

        return f


    def get_sem(self):
        if self.is_pronoun() == 1:
            if self.tokens[0][3] in ['he','she','you','i','me','her','him','his','hers','mine','us','ours','we']:
                return 1
            if self.tokens[0][3] in ['it','its']:
                return 0
            if self.tokens[0][3] in ['them','they','their']:
                return 2
        else:
            if self.tokens[0][10].strip("(*)") in ['NORP','PERSON']:
                return 1
            if self.tokens[0][10].strip("(*)") in ['TIME','GPE','ORG','CARDINAL','LOC','QUANTITY','DATE','FAC']:
                return 0
            else:
                return 2
        return 2

    
    def get_number(self):
        single = ['he', 'his', 'she', 'her', 'i', 'my', 'it', 'its', 'this', 'that']
        plural = ['they', 'their', 'our', 'us', 'these', 'those']

        if self.tokens[0][3] in single:
            return 1
        if self.tokens[0][3] in plural:
            return 2

        return 0

    
    def is_proper_noun(self):
        if self.tokens[0][4] in ['NNP', 'NNPS']:
            return 1
        
        return 0

        
    def is_definite(self):
        if self.tokens[0][3].lower() == 'the':
            return 1
        
        return 0

        
    def is_demos(self):
        if self.tokens[0][3].lower() in ['this', 'that', 'these', 'those']:
            return 1
        
        return 0


    def is_pronoun(self):
        if len(self.tokens) == 1:
            if self.tokens[0][4] in ['PRP', 'PRP$']:
                return 1
        return 0


# a pair of refexps from a doc to indicate if they refer to the same chain id/entity
class MarkablePair(object):

    def __init__(self, antecedent: Markable, anaphor: Markable, same_sent: int):
        self.antecedent = antecedent
        self.anaphor = anaphor

        self.label = True if antecedent.label == anaphor.label else False
        self.same_sentence = same_sent
        self.feat = self.features()

        
    def features(self):
        f = {}

        f['in_sentences'] = self.same_sentence

        f['antecedent_definite'] = self.antecedent.feat['definite']
        f['antecedent_demonstrative'] = self.antecedent.feat['demonstrative']
        f['antecedent_pronoun'] = self.antecedent.feat['pronoun']
        f['antecedent_proper_noun'] = self.antecedent.feat['proper_noun']
        f['antecedent_number'] = self.antecedent.feat['number']
        f['antecedent_sem'] = self.antecedent.feat['sem']
        f['antecedent_ner'] = self.antecedent.feat['named-entity']
        
        f['anaphor_definite'] = self.anaphor.feat['definite']
        f['anaphor_demonstrative'] = self.anaphor.feat['demonstrative']
        f['anaphor_pronoun'] = self.anaphor.feat['pronoun']
        f['anaphor_proper_noun'] = self.anaphor.feat['proper_noun']
        f['anaphor_number'] = self.anaphor.feat['number']
        f['anaphor_ner'] = self.anaphor.feat['named-entity']
        f['anaphor_sem'] = self.anaphor.feat['sem']

        # The last word of antecedent and anaphor match or not
        f['last_word_match'] = 1 if self.antecedent.feat['text'].split()[-1].lower() == self.anaphor.feat['text'].split()[-1].lower() else 0

        # Whether antecedent and anaphor are exactly the same in String
        f['string_match'] = 1 if self.antecedent.feat['text'] == self.anaphor.feat['text'] else 0

        # Same entity type
        f['ner_match'] = 1 if self.antecedent.feat['named-entity'] == self.anaphor.feat['named-entity'] else 0

        # number match
        f['number_match'] = self.number_match()

        # Substring
        f['substring'] = self.is_substring()

        #semantic class
        f['sem'] = 1 if self.antecedent.feat['sem'] == self.anaphor.feat['sem'] else 0

        return f


    def is_substring(self):
        f1 = self.antecedent.feat['text']
        f2 = self.anaphor.feat['text']

        if f1 in f2 or f2 in f1:
            return 1
        return 0


    def number_match(self):
        f1 = self.antecedent.feat['number']
        f2 = self.anaphor.feat['number']

        if f1 == f2:
            return 1

        return 0

