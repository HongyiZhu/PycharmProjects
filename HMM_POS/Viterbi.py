import nltk.tag.hmm as h
import pickle

from hmmlearn import hmm, base, utils



try:
    model = open("hmm_pretrain.pkl", 'rb')
    hmm = pickle.load(model)
    model.close()
except:
    pass

transitions = hmm._transitions
symbols = hmm._symbols
outputs = hmm._outputs
states = hmm._states
priors = hmm._priors
print(states)
print([priors.prob(x) for x in states])

