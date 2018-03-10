import argparse
import time

from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import f1_score
from sklearn.neural_network import MLPClassifier

from corpus import get_corpus
from get_files import generate_files


def main():
    parser = argparse.ArgumentParser(description='Run pairwise coreference resolution system')
    parser.add_argument('task', help='choose one task to go on: train/dev/test')
    parser.add_argument('-g', '--gold', default='gold.txt', help='gold file')
    parser.add_argument('-o', '--output', default='output.txt', help='output file')

    args = parser.parse_args()
    task = args.task
    gold = args.gold
    output = args.output

    path = {
        "dev": 'conll-2012/dev/english/annotations',
        "train": 'conll-2012/train/english/annotations',
        "test": 'conll-2012/test/english/annotations'
    }

    start = time.time()

    print("Parsing", task, "files...")
    X, y, corpus_data, corpus_pairs = get_corpus(path[task], train=True)\
                                      if task == "train" \
                                      else get_corpus(path[task], train=False)
    if task == "train":
        vec = DictVectorizer()
        vec.fit(X)
        print("Saving vec...")
        joblib.dump(vec, 'vec.pkl')

        print("Transforming data...")
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        X = vec.transform(X)

        print("Training model...")
        model = clf.fit(X, y)
        print("Saving model...")
        joblib.dump(model, 'model.pkl')

    else:
        print("Transforming data...")
        vec = joblib.load("vec.pkl")
        model = joblib.load("model.pkl")
        X = vec.transform(X)

        print("Predicting...")
        pred = model.predict(X)
        print("Pairwise classification F1:", f1_score(y, pred, average='macro'))
        pred = iter(pred.tolist())
        generate_files(corpus_data, corpus_pairs, pred, gold, output)

    end = time.time()

    print("Total time used: ", (end - start))


if __name__ == '__main__':
    main()