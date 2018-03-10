from collections import defaultdict


def generate_files(corpus_data, corpus_pairs, pred, gold, output):

    generate_help(gold, corpus_data, gold=True)

    for doc_pairs in corpus_pairs:
        for part_pairs in doc_pairs:
            guesses = [next(pred) for i in range(len(part_pairs))]
            chain_dict = get_chains(part_pairs, guesses)
            reduce_chain(chain_dict)
            modify_corpus(corpus_data, chain_dict)

    generate_help(output, corpus_data, gold=False)


def generate_help(name, corpus_data, gold):
    print("Generating", name, "file...")
    with open(name, "w") as f:
        for doc in corpus_data:
            for part in doc:
                for i, sent in enumerate(part):
                    if i == 0 or i == len(part) - 1:
                        f.write(" ".join(sent) + "\n")
                    else:
                        for word in sent:
                            f.write(" ".join(word) + "\n")
                            if gold:
                                word[-1] = "-"


def get_chains(part_pairs, guesses):
    chain_dict = defaultdict(set) # key: chain_id; value: a list of markable instances
    chain_id = 0  # we use the same chain id in data
    for i, pair in enumerate(part_pairs):
        guess = guesses[i]
        if guess:
            ante, anap = pair.antecedent, pair.anaphor

            # refexp_d = {}
            # for chain_id, mentions in chain_dict.items():
            #     if ante in mentions and ante not in refexp_d:
            #         refexp_d[ante] = chain_id
            #     if anap in mentions and anap not in refexp_d:
            #         refexp_d[anap] = chain_id
            #
            # if ante not in refexp_d and anap not in refexp_d:
            #     chain_dict[chain_id].add(ante)
            #     chain_dict[chain_id].add(anap)
            #     chain_id += 1
            # elif ante in refexp_d and anap not in refexp_d:
            #     chain = refexp_d[ante]
            #     chain_dict[chain].add(anap)
            # elif ante not in refexp_d and anap in refexp_d:
            #     chain = refexp_d[anap]
            #     chain_dict[chain].add(ante)
            # elif refexp_d[ante] != refexp_d[anap]:
            #     cid1, cid2 = (refexp_d[ante], refexp_d[anap]) if refexp_d[ante] < refexp_d[anap] \
            #                                                   else (refexp_d[anap], refexp_d[ante])
            #     chain_dict[cid1] = chain_dict[cid1].union(chain_dict[cid2])
            #     chain_dict[cid2] = set()


            # if ante not in chain_dict and anap not in chain_dict:
            #     chain_dict[ante] = chain_id
            #     chain_dict[anap] = chain_id
            #     chain_id += 1
            # elif anap not in chain_dict and ante in chain_dict:
            #     chain = chain_dict[ante]
            #     chain_dict[anap] = chain  # current anap will be ante for later refexps
            # elif anap in chain_dict and ante not in chain_dict:
            #     chain = chain_dict[anap]
            #     chain_dict[ante] = chain
            # elif anap in chain_dict and ante in chain_dict:
            #     print(chain_dict[anap] == chain_dict[ante])

            chain = find(chain_dict, ante, anap)
            if chain == -1:
                chain_dict[chain_id].add(ante)
                chain_dict[chain_id].add(anap)
                chain_id += 1
            else:
                chain_dict[chain].add(ante)
                chain_dict[chain].add(anap)

    return chain_dict


def find(chain_dict, ante, anap):
    for chain_id, mentions in chain_dict.items():
        if ante in mentions or anap in mentions:
            return chain_id
    return -1


def reduce_chain(chain_dict):
    mention_set = set()
    for chain_id, mentions in chain_dict.items():
        id_mentions = set()
        for m in mentions:
            if m not in mention_set:
                mention_set.add(m)
                id_mentions.add(m)
        chain_dict[chain_id] = id_mentions


def modify_corpus(corpus_data, chain_dict):
    for chain_id, mentions in chain_dict.items():
        print(chain_id, [m.span for m in mentions],
              [m.label for m in mentions],
              [m.feat["text"] for m in mentions],
              [m.position for m in mentions])

        for m in mentions:
            doc_id, part_id, sent_id = m.position
            start, end = m.span

            start_tag = corpus_data[doc_id][part_id][sent_id][start][-1]
            if start_tag == "-":
                corpus_data[doc_id][part_id][sent_id][start][-1] = "(" + str(chain_id)
            else:
                corpus_data[doc_id][part_id][sent_id][start][-1] += "|(" + str(chain_id)

            end_tag = corpus_data[doc_id][part_id][sent_id][end][-1]
            if end_tag == "-":
                corpus_data[doc_id][part_id][sent_id][end][-1] = str(chain_id) + ")"
            elif start == end:
                corpus_data[doc_id][part_id][sent_id][end][-1] += ")"
            else:
                corpus_data[doc_id][part_id][sent_id][end][-1] = str(chain_id) + ")|" + end_tag

