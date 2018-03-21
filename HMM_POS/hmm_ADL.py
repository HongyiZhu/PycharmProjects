import pickle
import numpy as np
from hmmlearn import hmm as h2
from scipy.optimize import linear_sum_assignment
import warnings

__author__ = 'Hongyi Zhu'

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

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
f = open("x.txt", "rb")
g = open("y.txt", "rb")
x = pickle.load(f)
y = pickle.load(g)
f.close()
g.close()

x_token = [0, 3, 4, 5, 6, 9, 10, 15, 16, 19, 20]

x_train = []
y_train = []
for i in range(800):
    for e in x[i]:
        x_train.append([x_token.index(e)])
    for e in y[i]:
        y_train.append([e])
lengths_train = [500] * 800

x_test = []
y_test = []
for i in range(100):
    for e in x[i]:
        x_test.append([x_token.index(e)])
    for e in y[i]:
        y_test.append([e])
lengths_test = [500] * 100

try:
    model = open("hmm_ADL.pkl", 'rb')
    hmm = pickle.load(model)
    model.close()
except:
    hmm = h2.MultinomialHMM(n_components=4, tol=1e-4, verbose=True, n_iter=2000) \
            .fit(x_train, lengths=lengths_train)

model = open("hmm_ADL.pkl", 'wb')
pickle.dump(hmm, model)
model.close()

# initial decoding
tag = hmm.predict(x_test, lengths=lengths_test)
tag_dict = {0:0,21:1,22:2,23:3}
# Get confusion matrix
conf_matrix = np.empty((4, 4), np.int32)
conf_matrix.fill(0)
for i in range(len(tag)):
    conf_matrix[tag[i], tag_dict[y_test[i][0]]] += 1

# Assigns hidden states clusters to known states to maximize the accuracy
# and re-map the decoded result
cluster_dict = dict((x, i) for x, i in enumerate(_assign(conf_matrix)))
transformed_predict = [cluster_dict[x] for x in tag]

# Calculate accuracy
same = 0
zero = 0
for i in range(len(tag)):
    if transformed_predict[i] == tag_dict[y_test[i][0]]:
        same += 1
    if tag_dict[y_test[i][0]] == 0:
        zero += 1
print(zero)
print("Accuracy1:\t" + str(same / len(tag)))
print("Accuracy2:\t" + str(_assign2(conf_matrix)/len(tag)))