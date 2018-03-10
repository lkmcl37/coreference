import os
from collections import defaultdict
from feature import *


# parse each raw file and extract features
def get_corpus(path, train=True):
    X = []  # the refexp pairs in the whole corpus, all docs
    y = []
    corpus_data = []
    corpus_pairs = []
    doc_id = 0

    end_str = "auto_conll" if train else "gold_conll"

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(end_str):
                X_temp, y_temp, doc_data, doc_pairs = parse_file(os.path.join(root, file), doc_id)
                X.extend(X_temp)
                y.extend(y_temp)
                corpus_data.append(doc_data)
                corpus_pairs.append(doc_pairs)
                doc_id += 1

    return X, y, corpus_data, corpus_pairs


# helper function for parsing ONE auto_conell file (one doc)
def parse_file(path, doc_id):
    part = []
    sent = []
    doc = []

    with open(path, 'r', encoding="utf8") as f:
        for line in f:
            line = line.strip('\n')
            if not line:
                if sent:
                    part.append(sent)
                    sent = []
                continue

            # a new part in one doc
            if line.startswith('#begin'):
                part = [line.split()]
                sent = []
                continue
            # the end of current part in one doc
            elif line == '#end document':
                part.append(line.split())
                doc.append(part)
            else:
                fields = line.split()
                sent.append(fields)

    X = []  # the refexp pairs in this doc
    y = []  # the labels indicating if the pair refers to the same entity
    doc_pairs = []
    for part_id, part in enumerate(doc):
        # the refexp pairs in this part
        part_pairs = get_pairs(part, part_id, doc_id)
        doc_pairs.append(part_pairs)
        # append part pairs to doc pair list
        X.extend([p.feat for p in part_pairs])
        y.extend([p.label for p in part_pairs])

    return X, y, doc, doc_pairs


# pair all extracted mentions with all possible combinations in one part
# to create positive and negative train instances
def get_pairs(part, part_id, doc_id):
    pairs = []
    part_mentions = []

    for sent_id in range(1, len(part) - 1, 1):
        sent_mentions = get_metions(doc_id, part_id, sent_id, part[sent_id])
        part_mentions.append(sent_mentions)

    for i, sent_mentions in enumerate(part_mentions):
        for j, antecedent in enumerate(sent_mentions):
            pairs.extend([MarkablePair(antecedent, anaphor, 1) for anaphor in sent_mentions[j + 1:]])
            for next_sent_mentions in part_mentions[i + 1:]:
                pairs.extend([MarkablePair(antecedent, anaphor, 0) for anaphor in next_sent_mentions])

    return pairs


# parse the coreference fields of the file and obtain the mentions
def get_metions(doc_id, part_id, sent_id, tokens):
    
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
            mentions.append(Markable(tokens[s:i+1], (s,i), j, doc_id, part_id, sent_id))

    # the mentions are already in order according to their appearances in the sentence
    return mentions
