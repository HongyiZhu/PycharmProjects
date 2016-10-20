import nltk.tag.hmm as h

__author__ = 'Hongyi Zhu'


def read_corpus():
    f = open('corpus.it', 'r')
    # all the tokens in the corpus
    tokens = set()
    # all the labels in the corpus
    labels = set()
    # the dict containing training sentences and tags
    sentences = {}
    st = ['<s>']
    tags = ['<S>']
    for lines in f:
        if not lines.strip() == "":
            [t, l] = lines.strip().split("\t")
            tokens.add(t)
            labels.add(l)
            st.append(t)
            tags.append(l)
        else:
            st.append('</s>')
            tags.append('</S>')
            sent = " ".join(st)
            tag = " ".join(tags)
            sentences[sent] = tag
            st = ['<s>']
            tags = ['<S>']
    return list(tokens), list(labels), sentences

def main():
    read_corpus()
    trainer = h.HiddenMarkovModelTrainer()
    hmm =  trainer.train_unsupervised()

if __name__ == 'main':
    main()

tokens, labels, sentences = read_corpus()
labels.append('<S>')
labels.append('</S>')
trainer = h.HiddenMarkovModelTrainer(labels, tokens)
hmm =  trainer.train_unsupervised(list(sentences.keys()))



