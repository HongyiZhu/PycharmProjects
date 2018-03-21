import os
import click

import pickle
import numpy as np
from keras.layers.recurrent import GRU
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, RepeatVector


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = 'models'

MODEL_STRUCT_FILE = 'piglatin_struct.json'
MODEL_WEIGHTS_FILE = 'piglatin_weights.h5'

DATA_PATH = 'data'
WORDS_FILE = 'words.txt'
CHAR_SET = ['a','b','c','d','e','f','g','h','i','j','k','A','B','C','D']
CHAR_NUM = len(CHAR_SET)
CHAR_TO_INDICES = {c:i for i, c in enumerate(CHAR_SET)}
INDICES_TO_CHAR = {i:c for c, i in CHAR_TO_INDICES.items()}
MAX_INPUT_LEN = 500
MAX_OUTPUT_LEN = 500

def vectorize(word, seq_len, vec_size):
    vec = np.zeros((seq_len, vec_size), dtype=int)
    for i, ch in enumerate(word):
        vec[i, CHAR_TO_INDICES[ch]] = 1

    return vec

dic_x = {
    0: 'k',
    3: 'a',
    4: 'b',
    5: 'c',
    6: 'd',
    9: 'e',
    10: 'f',
    15: 'g',
    16: 'h',
    19: 'i',
    20: 'j'
}

dic_y = {
    0 : 'A',
    21 : 'B',
    22 : 'C',
    23 : 'D'
}

def build_data():
    f = open("x.txt", "rb")
    g = open("y.txt", "rb")
    x = pickle.load(f)
    y = pickle.load(g)
    f.close()
    g.close()

    plain_x = []
    plain_y = []
    for w in range(len(x)):
        seq_x = x[w]
        transformed_x = [dic_x[i] for i in seq_x]
        word_x = ''.join(transformed_x)
        plain_x.append(word_x)
        seq_y = y[w]
        transformed_y = [dic_y[i] for i in seq_y]
        word_y = ''.join(transformed_y)
        plain_y.append(word_y)

    train_x = np.zeros((len(x), MAX_INPUT_LEN, CHAR_NUM), dtype=int)
    train_y = np.zeros((len(x), MAX_OUTPUT_LEN, CHAR_NUM), dtype=int)
    for i in range(len(x)):
        train_x[i] = vectorize(plain_x[i], MAX_INPUT_LEN, CHAR_NUM)
        train_y[i] = vectorize(plain_y[i], MAX_OUTPUT_LEN, CHAR_NUM)

    return train_x, train_y


def build_model_from_file(struct_file, weights_file):
    model = model_from_json(open(struct_file, 'r').read())
    model.compile(loss="mse", optimizer='adam')
    model.load_weights(weights_file)

    return model


def build_model(input_size, seq_len, hidden_size):
    model = Sequential()
    model.add(GRU(input_dim=input_size, output_dim=hidden_size, return_sequences=False))
    model.add(Dense(hidden_size, activation="relu"))
    model.add(RepeatVector(seq_len))
    model.add(GRU(hidden_size, return_sequences=True))
    model.add(TimeDistributed(Dense(output_dim=input_size, activation="linear")))
    model.compile(loss="mse", optimizer='adam')

    return model


def save_model_to_file(model, struct_file, weights_file):
    # save model structure
    model_struct = model.to_json()
    open(struct_file, 'w').write(model_struct)

    # save model weights
    model.save_weights(weights_file, overwrite=True)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--epoch', default=100, help='number of epoch to train model')
@click.option('-m', '--model_path', default=os.path.join(PROJECT_ROOT, MODEL_PATH), help='model files to save')
def train(epoch, model_path):
    x, y = build_data()
    train_x = x[:800]
    train_y = y[:800]
    tune_x = x[800:900]
    tune_y = y[800:900]

    model = build_model(CHAR_NUM, MAX_OUTPUT_LEN, 128)

    model.fit(train_x, train_y, validation_data=(tune_x, tune_y), batch_size=128, nb_epoch=epoch)

    struct_file = os.path.join(model_path, MODEL_STRUCT_FILE)
    weights_file = os.path.join(model_path, MODEL_WEIGHTS_FILE)

    save_model_to_file(model, struct_file, weights_file)


@cli.command()
@click.option('-m', '--model_path', default=os.path.join(PROJECT_ROOT, MODEL_PATH), help='model files to read')
def test(model_path, word):
    x, y = build_data()
    test_x = x[900:]
    test_y = y[900:]

    struct_file = os.path.join(model_path, MODEL_STRUCT_FILE)
    weights_file = os.path.join(model_path, MODEL_WEIGHTS_FILE)

    model = build_model_from_file(struct_file, weights_file)

    same_count = 0
    for i in range(100):
        x = np.zeros((1, MAX_INPUT_LEN, CHAR_NUM), dtype=int)
        x[0] = vectorize(test_x[i], MAX_INPUT_LEN, CHAR_NUM)

        pred = model.predict(x)[0]
        seq = ''.join([
            INDICES_TO_CHAR[i] for i in pred.argmax(axis=1)
        ])
        lab = test_y[i]
        for j in range(len(seq)):
            if seq[j] == lab[j]:
               same_count += 1
    print("Accuracy:\t",str(same_count/5000.0))

if __name__ == '__main__':
    cli()