

class Markable(object):
    def __init__(self, tokens, span, label, doc_id, part_id, sent_id):
        self.tokens = tokens  # tokens are the segment of refexp
        self.span = span      # start and end in span are inclusive

        self.label = label    # coref chain id of this refexp
        self.position = (doc_id, part_id, sent_id)

        self.feat = self.features()

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

        return f

    def get_number(self):
        single = ['he', 'his', 'she', 'her', 'i', 'my', 'it', 'its', 'this', 'that']
        plural = ['they', 'their', 'our', 'us', 'these', 'those']

        if self.tokens[0][3] in single:
            return 1
        if self.tokens[0][3] in plural:
            return 2

        return 0
    
    def is_proper_noun(self):
        for t in self.tokens:
            if t[4] in ['NNP', 'NNPS']:
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

        # f['antecedent_text'] = self.antecedent.feat['text']
        # f['antecedent_NE'] = self.antecedent.feat['named-entity']
        f['antecedent_definite'] = self.antecedent.feat['definite']
        f['antecedent_demonstrative'] = self.antecedent.feat['demonstrative']
        f['antecedent_pronoun'] = self.antecedent.feat['pronoun']
        f['antecedent_proper_noun'] = self.antecedent.feat['proper_noun']
        
        # f['anaphor_text'] = self.anaphor.feat['text']
        # f['anaphor_NE'] = self.anaphor.feat['named-entity']
        f['anaphor_definite'] = self.anaphor.feat['definite']
        f['anaphor_demonstrative'] = self.anaphor.feat['demonstrative']
        f['anaphor_pronoun'] = self.anaphor.feat['pronoun']
        f['anaphor_proper_noun'] = self.anaphor.feat['proper_noun']

        # The last word of antecedent and anaphor match or not
        f['last_word_match'] = 1 if self.antecedent.feat['text'].split()[-1] == self.anaphor.feat['text'].split()[-1] else 0

        # Whether antecedent and anaphor are exactly the same in String
        f['string_match'] = 1 if self.antecedent.feat['text'] == self.anaphor.feat['text'] else 0

        # Same entity type
        f['ner_match'] = 1 if self.antecedent.feat['named-entity'] == self.anaphor.feat['named-entity'] else 0

        # number match
        f['number_match'] = self.number_match()

        # Substring
        f['substring'] = self.is_substring()

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

        # if f1 == 2 or f2 == 2:
        #     return 2
        if f1 == f2:
            return 1

        return 0

