#%%
# dataloader source code
import gzip
import numpy as np
from pathlib import Path
import math

## Utils ##
def read_glove_vecs(self, path):
    with open(path, 'r', encoding = "utf8") as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word]
            word_to_vec_map[curr_word] = np.array(line[1:], dtype = np.float64)
        i = 1
        word_to_idx = {}
        idx_to_words = {}
        for w in sorted(words):
            word_to_idx[w] = i
            idx_to_words[i] = w
            i = i+1
    return word_to_idx, idx_to_words, word_to_vec_map

def sentences_to_indices(x, w_2_i, maxlen):
    m = x.shape[0]
    x_indices = np.zeros((m, maxlen))
    for i in range(m):
        words = (x[i].lower()).split()
        j = 0
        for w in words:
            x_indices[i,j] = w_2_i[w]
            j += 1
    return x_indices

## DATA LOADER ##
class Dataloader():
    def __init__(self, path, word_to_idx, is_train=True, shuffle=True, batch_size=8):
        path = Path(path)
        datapath = Path(path/'train_emoji.csv') if is_train else Path(path/'test_emoji.csv')
        self.batch_size = batch_size
        self.sentences, self.labels = self.loadData(datapath, word_to_idx)
        self.index = 0
        self.idx = np.arange(0, self.sentences.shape[0])
        if shuffle: np.random.shuffle(self.idx) # shuffle images
        self.maxlen = 0

    def __len__(self):
        n_sentences, _, _, _ = self.sentences.shape
        n_sentences = math.ceil(n_sentences / self.batch_size)
        return n_sentences

    def __iter__(self):
        return datasetIterator(self)

    def __getitem__(self, index):
        x = self.sentences[self.idx[index * self.batch_size:(index + 1) * self.batch_size]]
        y = self.labels[self.idx[index * self.batch_size:(index + 1) * self.batch_size]]
        
        return x, y

    ## DataLoad
    def loadData(self, path, word_to_idx):
        emoji = pd.read_csv(path, names = ['sentence', 'label'], header=None, usecols = [1,0])
        
        # load sentence data
        x = np.array(emoji.sentence)
        maxlen = len(max(x, key = len).split())
        self.maxlen = maxlen
        x_indices = self.sentences_to_indices(x, word_to_idx, maxlen)
        
        # load label in one-hot encoding
        y = np.array(emoji.label)
        rows = len(y)
        cols = y.max() + 1
        one_hot = np.zeros((rows, cols)).astype(np.uint8)
        one_hot[np.arange(rows), y] = 1
        one_hot = one_hot.astype(np.float64)

        return x_indices, one_hot

# for enumerate magic python function returns Iterator
class datasetIterator():
    def __init__(self, dataloader):
        self.index = 0
        self.dataloader = dataloader

    def __next__(self):
        if self.index < len(self.dataloader):
            item = self.dataloader[self.index]
            self.index += 1
            return item
        # end of iteration
        raise StopIteration

#%%
class myRNN():
    def __init__(cell_mode, op_mode, embd_d, hidden_d, output_d, dropout = 0)
        """
        cell_mode: 0(Vanilla RNN), 1(LSTM)
        op_mode: optimization mode. 0(SGD), 1(ADAM)
        embd_d: embedding dimension 50 or 100
        hidden_d: 128 or 256
        output_d: 4
            0 -- heart
            1 -- baseball
            2 -- smile
            3 -- disappointed
            4 -- fork_and_knife 
        dropout: default = 0.
        """

    def rnn_cell_forward(self, xt, hidden, params):
        """
        xt: input data at timestep t. shape = (n_x, m)
        hidden: hidden state at timestep t-1. shape = (n_a, m)
        params: dictionary containing parameters
            W_xh -- wegith matrix mult the input. shape (n_a,n_x)
            W_hh -- weight matrix mult the hidden state. shape(n_a, n_a)
            W_hy -- weight matrix relating the hidden-state to the output. n_y, n_a
        returns...
        h_next -- next hidden state
        yt_pred -- prediction at timestep"t"
        cache -- tuple of values needed for backward pass. (h_next, hidden, xt, params)
        """
        W_xh = params["W_xh"]
        W_hh = params["W_hh"]
        W_hy = params["W_hy"]
        bh = params["bh"]
        by = params["by"]

        h_next = np.tanh(W_xh.dot(xt) + W_hh.dot(hidden)+bh))
        yt_pred = self.softmax(W_hy.dot(hidden) + by)

        cache = (h_next, hidden, xt, params)

        return h_next, yt_pred, cache

    
    def __init__(self, rnn_units, input_dim, output_dim):
        super(RNN, self).__init__()

        #initialize weight matrices
        self.W_xh = self.add_weight([rnn_units, input_dim])
        self.W_hh = self.add_weight([rnn_units, rnn_units])
        self.W_hy = self.add_weight([output_dim, rnn_units])

        #initialize hidden state to xeros
        self.h = tf.seros([rnn_units,1])

def SentimentAnalysis(input_shape, word_to_vec_map, word_to_index):
    """
    Function creating the Emojify-v2 model's graph.
    Arguments:
    input_shape -- shape of the input, usually (max_len,)
    word_to_vec_map -- dictionary mapping every word in a vocabulary into its 50-dimensional vector representation
    word_to_index -- dictionary mapping from words to their indices in the vocabulary (400,001 words)
    Returns:
    model -- a model instance in Keras
    """
    # Define sentence_indices as the input of the graph, it should be of shape input_shape and dtype 'int32' (as it contains indices).
    sentence_indices = Input(shape=input_shape, dtype=np.int32)

    # Create the embedding layer pretrained with GloVe Vectors (≈1 line)
    embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index)

    # Propagate sentence_indices through your embedding layer, you get back the embeddings
    embeddings = embedding_layer(sentence_indices)

    # Propagate the embeddings through an LSTM layer with 128-dimensional hidden state
    # Be careful, the returned output should be a batch of sequences.
    X = LSTM(128, return_sequences=True)(embeddings)
    # Add dropout with a probability of 0.5
    X = Dropout(0.5)(X)
    # Propagate X trough another LSTM layer with 128-dimensional hidden state
    # Be careful, the returned output should be a single hidden state, not a batch of sequences.
    X = LSTM(128)(X)
    # Add dropout with a probability of 0.5
    X = Dropout(0.5)(X)
    # Propagate X through a Dense layer with softmax activation to get back a batch of 5-dimensional vectors.
    X = Dense(5, activation='softmax')(X)
    # Add a softmax activation
    X = Activation('softmax')(X)

    # Create Model instance which converts sentence_indices into X.
    model = Model(sentence_indices, X)

    return model

    
# set parameters
param={'cell' = 0, 'optimizer'=0, "glove"= 50, 'dropout' = 0}

# training and getting result
if __name__ == "__main__":
    # load data
    glove_size = param["glove"]
    glovepath = Path(path/'glove.6B.50d.txt') if glove_size == 50 else PathPath(path/'glove.6B.100d.txt')
    word_to_idx, i_2_w, word_to_vec_map = read_glove_vecs(glove_path)

    trainLoad = Dataloader(path = '/home/artiv',  glove_size = 50, is_train = True, word_to_idx = w_2_i)
    testLoad = Dataloader(path = '/home/artiv', batch_size = 1, is_train = False, shuffle=False, word_to_idx = w_2_i)

    model = myRNN((trainLoad.maxlen, word_to_vec_map, word_to_idx)) # input shape, word_2_ve_map, word_to_idx


