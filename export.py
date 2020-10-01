import numpy as np

import directories
import utils
import pairwise_models
import clustering_models
import word_vectors

"""
Exports a model into a form readable by CoreNLP.
"""

def write_word_vectors(model, path):
    w = word_vectors.WordVectors(load=True)
    w.vectors = np.asarray(pairwise_models.get_weights(model, 'final_weights')[0])
    write_vectors(w, path + 'vectors_learned')

    w = word_vectors.WordVectors(keep_all_words=True)
    write_vectors(w, path + 'vectors_pretrained_all')


def write_weights(model, path):
    weights = pairwise_models.get_weights(model, 'final_weights')

    w_ana = clustering_models.anaphoricity_weights(weights)
    write_matrices(w_ana, path + 'anaphoricity_weights')

    w_pair = clustering_models.pair_weights(weights)
    first = w_pair[0]
    s = 832 if directories.CHINESE else 650
    write_matrices([first[:s, :], first[s:2 * s, :], first[2 * s:, :]] + w_pair[1:],
                   path + 'pairwise_weights')


def write_vectors(vectors, path):
    with open(path, 'wb') as f:
        for w, i in vectors.vocabulary.items():
            if w == word_vectors.UNKNOWN_TOKEN:
                w = "*UNK*"
            f.write((w + " " + " ".join(map(str, vectors.vectors[i])) + "\n").encode('utf-8'))

def write_matrices(ms, fname):
    print("Writing matrices to " + fname)
    print([m.shape for m in ms])
    with open(fname, 'w') as f:
        for m in ms:
            if len(m.shape) == 1:
                f.write(" ".join(map(str, m)) + "\n")
            else:
                for i in range(m.shape[0]):
                    f.write(" ".join(map(str, m[i])) + "\n")
            f.write("\n\n")

if __name__ == '__main__':
    path = directories.MODELS + "reward_rescaling/exported_weights/"
    utils.mkdir(path)
    write_word_vectors("reward_rescaling", path)
    write_weights("reward_rescaling", path)
