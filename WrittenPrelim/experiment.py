import numpy as np
np.random.seed(1024)  # for reproducibility

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD



