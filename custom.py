from Bio import SeqIO
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from collections import Counter
from copy import deepcopy

def load_sequence_and_metadata():
    """
    Returns the sequences as a list of SeqRecords, and metadata as a pandas DataFrame.
    """
    
    sequences = [s for s in SeqIO.parse('data/20170531-H3N2-global.fasta', 'fasta')]
    
    metadata = pd.read_csv('data/20170531-H3N2-global.tsv', sep='\t', parse_dates=['Collection Date'])
    
    return sequences, metadata


def right_pad(sequences):
    """
    Pads sequences with extra "*" characters.
    """
    padded_sequences = deepcopy(sequences)
    seq_lengths = compute_seq_lengths(sequences)
    
    for s in padded_sequences:
        while len(s) < max(seq_lengths.keys()):
            s.seq += '*'
    return padded_sequences


def compute_seq_lengths(sequences):
    """
    Computes the sequence lengths.
    """
    seq_lengths = [len(s) for s in sequences]
    seq_lengths = Counter(seq_lengths)
    return seq_lengths

    
def seq2chararray(sequences):
    """
    Returns sequences coded as a numpy array. Doesn't perform one-hot-encoding.
    """
    padded_sequences = right_pad(sequences)
    seq_lengths = compute_seq_lengths(sequences)
    char_array = np.chararray(shape=(len(sequences), max(seq_lengths.keys())), unicode=True)
    for i, seq in enumerate(padded_sequences):
        char_array[i, :] = list(seq)
    return char_array


def compute_alphabet(sequences):
    """
    Returns the alphabet used in a set of sequences.
    """
    alphabet = set()
    for s in sequences:
        alphabet = alphabet.union(set(s))
        
    return alphabet


def encode_array(sequences):
    """
    Performs binary encoding of the sequence array.
    
    Inputs:
    =======
    - seq_array: (numpy array) of characters.
    - seq_lengths: (Counter) dictionary; key::sequence length; value::number of sequences with that length.
    """
    # Binarize the features to one-of-K encoding.
    alphabet = compute_alphabet(sequences)
    seq_lengths = compute_seq_lengths(sequences)
    seq_array = seq2chararray(sequences)
    lb = LabelBinarizer()
    lb.fit(list(alphabet))

    encoded_array = np.zeros(shape=(seq_array.shape[0], max(seq_lengths.keys()) * len(alphabet)))

    for i in range(seq_array.shape[1]):
        encoded_array[:, i*len(alphabet):(i+1)*len(alphabet)] = lb.transform(seq_array[:, i])

    return encoded_array
