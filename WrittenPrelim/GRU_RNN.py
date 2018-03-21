import os
import re
import string
from itertools import dropwhile

import numpy as np
from keras.layers.recurrent import GRU
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, RepeatVector

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = 'models'

MODEL_STRUCT_FILE = 'piglatin_struct.json'
MODEL_WEIGHTS_FILE = 'piglatin_weights.h5'

MAX_INPUT_LEN = 500

def train(epoch, model_path):
    x, y = build_data()
    test_x = x[:indices]
    test_y = y[:indices]
    train_x = x[indices:]
    train_y = y[indices:]

    model = build_model(CHAR_NUM, 500, 128)

    model.fit(train_x, train_y, validation_data=(test_x, test_y), batch_size=128, nb_epoch=epoch)

    struct_file = os.path.join(model_path, MODEL_STRUCT_FILE)
    weights_file = os.path.join(model_path, MODEL_WEIGHTS_FILE)

    save_model_to_file(model, struct_file, weights_file)

def build_model(input_size, seq_len, hidden_size):
    model = Sequential()
    model.add(GRU(input_dim=input_size, output_dim=hidden_size, return_sequences=False))
    model.add(Dense(hidden_size, activation="relu"))
    model.add(RepeatVector(seq_len))
    model.add(GRU(hidden_size, return_sequences=True))
    model.add(TimeDistributed(Dense(output_dim=input_size, activation="linear")))
    model.compile(loss="mse", optimizer='adam')
    return model

def build_model_from_file(struct_file, weights_file):
    model = model_from_json(open(struct_file, 'r').read())
    model.compile(loss="mse", optimizer='adam')
    model.load_weights(weights_file)

    return model

def test(model_path, word):
    struct_file = os.path.join(model_path, MODEL_STRUCT_FILE)
    weights_file = os.path.join(model_path, MODEL_WEIGHTS_FILE)

    model = build_model_from_file(struct_file, weights_file)

    x = np.zeros((1, MAX_INPUT_LEN, CHAR_NUM), dtype=int)
    word = BEGIN_SYMBOL + word.lower().strip() + END_SYMBOL
    x[0] = vectorize(word, MAX_INPUT_LEN, CHAR_NUM)

    pred = model.predict(x)[0]
    print(''.join([
        INDICES_TO_CHAR[i] for i in pred.argmax(axis=1)
        if INDICES_TO_CHAR[i] not in (BEGIN_SYMBOL, END_SYMBOL)
    ]))