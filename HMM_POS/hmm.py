import nltk.tag.hmm as h
import pickle
import sys

__author__ = 'Hongyi Zhu'


def read_corpus():
    f = open('corpus.it', 'r')
    # all the tokens in the corpus
    tokens = set()
    # all the labels in the corpus
    labels = set()
    # the dict containing training sentences and tags
    sentences = []
    st = []
    for lines in f:
        if not lines.strip() == "":
            [t, l] = lines.strip().split("\t")
            tokens.add(t)
            labels.add(l)
            st.append((t,l))
        else:
            sentences.append(st)
            st = []
    f.close()

    return list(tokens), list(labels), sentences


def main():
    # load corpus
    tokens, labels, sentences = read_corpus()
    trainer = h.HiddenMarkovModelTrainer(labels, tokens)

    # load model
    hmm = None
    try:
        model = open("hmm_pretrain.pkl", 'rb')
        hmm = pickle.load(model)
        model.close()
    except:
        pass

    # training model
    hmm = trainer.train_unsupervised(list(sentences), max_iterations=2, model=hmm)

    # save model
    model = open("hmm_pretrain.pkl", 'wb')
    pickle.dump(hmm, model)
    model.close()

    # test the trained model
    hmm.test(list(sentences[:10]),verbose=True)

if __name__ == 'main':
    main()

main()