import pickle
import numpy as np
from hmmlearn import hmm as h2
from scipy.optimize import linear_sum_assignment
import warnings
import argparse

__author__ = 'Hongyi Zhu'

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

def _read_corpus():
    f = open('corpus.it', 'r')
    # all the tokens in the corpus
    lower_tokens = set()
    # tokens = set()
    # all the labels in the corpus
    labels = set()
    # the dict containing training sentences and tags
    sentences = []
    st = []
    for lines in f:
        if not lines.strip() == "":
            [t, l] = lines.strip().split("\t")
            lower_tokens.add(t.lower())
            # tokens.add(t)
            labels.add(l)
            st.append((t.lower(),l))
        else:
            sentences.append(st)
            st = []
    f.close()
    print(len(lower_tokens))
    # print(len(tokens))
    lower_tokens = sorted(list(lower_tokens))
    labels = sorted(labels)

    return list(lower_tokens), list(labels), sentences

def _generate_data():
    tokens, labels, sentences = _read_corpus()
    reverse_token_index = dict([(x, i) for x, i in enumerate(tokens)])
    token_to_index = dict([(i, x) for x,i in enumerate(tokens)])
    reverse_label_to_index = dict([(x, i) for x, i in enumerate(labels)])
    label_to_index = dict([(i, x) for x, i in enumerate(labels)])
    sentence_pack = []
    length_pack = []
    tag_pack = []

    for sentence in sentences:
        length_pack.append(len(sentence))
        for (word, tag) in sentence:
            sentence_pack.append([int(token_to_index[word.lower()])])
            tag_pack.append(int(label_to_index[tag]))

    return token_to_index, reverse_token_index, label_to_index, reverse_label_to_index, sentence_pack, length_pack, tag_pack

def _recover(predict_tag_pack, length_pack, sentence_pack, reverse_label_to_index, reverse_token_index, tag_pack):
    index = 0
    for length in length_pack:
        st = sentence_pack[index: index+length]
        pred = predict_tag_pack[index: index+length]
        tag = tag_pack[index: index+length]
        output1 = [reverse_token_index[x]+"/"+reverse_label_to_index[y] for ([x], y) in zip(st, pred)]
        output2 = [reverse_token_index[x] + "/" + reverse_label_to_index[y] for ([x], y) in zip(st, tag)]
        print("Predict:  " + " ".join(output1))
        print("Original: " + " ".join(output2))
        print()
        index += length
    return None

def _assign(confusion_matrix):
    cost_matrix = np.max(confusion_matrix) - confusion_matrix
    return linear_sum_assignment(cost_matrix)[1]

def _assign2(confusion):
    a = 0
    for i in range(11):
        r, c = np.unravel_index(np.argmax(confusion),confusion.shape)
        a += confusion[r,c]
        confusion[r,:] = -1
        confusion[:,c] = -1
    return a


def main(load=True,verbose=False):
    # load corpus
    token_to_index, reverse_token_to_index, label_to_index, reverse_label_to_index, \
    sentence_pack, length_pack, tag_pack = _generate_data()

    # open model
    if load:
        # load model
        hmm = None
        try:
            model = open("hmm_pretrain.pkl", 'rb')
            hmm = pickle.load(model)
            model.close()
        except:
            hmm = h2.MultinomialHMM(n_components=len(label_to_index), tol=1e-6, verbose=True, n_iter=1000000)\
                .fit(sentence_pack, lengths=length_pack)
    else:
        hmm = h2.MultinomialHMM(n_components=len(label_to_index), tol=1e-6, verbose=True, n_iter=1000000) \
            .fit(sentence_pack, lengths=length_pack)

    # initial decoding
    tag = hmm.predict(sentence_pack, lengths=length_pack)

    # Get confusion matrix
    conf_matrix = np.empty((11, 11), np.int32)
    conf_matrix.fill(0)
    for i in range(len(tag)):
        conf_matrix[tag[i], tag_pack[i]] += 1

    # Assigns hidden states clusters to known states to maximize the accuracy
    # and re-map the decoded result
    cluster_dict = dict((x, i) for x, i in enumerate(_assign(conf_matrix)))
    transformed_predict = [cluster_dict[x] for x in tag]

    # Print the recovered sentences tagging
    if verbose:
        _recover(transformed_predict, length_pack, sentence_pack,
                reverse_label_to_index, reverse_token_to_index, tag_pack)

    # Calculate accuracy
    same = 0
    for i in range(len(tag)):
        if transformed_predict[i] == tag_pack[i]:
            same += 1
    print("Accuracy1:\t" + str(same / len(tag)))
    print("Accuracy2:\t" + str(_assign2(conf_matrix)/len(tag)))

    # clean up and save model
    if not load:
        model = open("hmm_newlytrained.pkl", 'wb')
        pickle.dump(hmm, model)
        model.close()

parser = argparse.ArgumentParser(description='HMM Tagger.')
parser.add_argument('-t', '--train', action='store_false',
                    help='Train a new HMM model.')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Print the original & tagged sentences.')
args = parser.parse_args()
main(args.train, args.verbose)