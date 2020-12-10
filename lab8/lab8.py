import nltk
import re
import numpy as np
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN, AgglomerativeClustering

import json
import pickle

sentence_detector=nltk.data.load("tokenizers/punkt/english.pickle")

print(stopwords.words('english'))

# random sentecnce with lot of stop words
# sample_text = "Oh man, this is pretty cool. We will do more such things."
# text_tokens = word_tokenize(sample_text)

# tokens_without_sw = [word for word in text_tokens if not word in stopwords.words('english')]
#
# print(text_tokens)
# print(tokens_without_sw)

def read(filename):
    f=open(filename,"r")
    text=f.read()
    f.close()
    return text



def preprocess(text):
    #eliminare referinte
    text=re.sub("\[\d*\]","",text)
    text=re.sub("-?\d+(?:\.\d+)?%?","nrnr",text)
    text=text.replace(",","")
    print(text)
    #impartire in prop- automat utilizand punkt + toLOWER
    sentences=sentence_detector.tokenize(text.strip().lower())
    sentence_tokens=[]
    unique_words=set()
    for s in sentences:
        print(s)
        s=re.sub("[\.\(\)\:]","",s)
        #tokenizare
        text_tokens=word_tokenize(s)
        print(text_tokens)
        #eliminare stop words
        tokens_without_sw = [word for word in text_tokens if word not in stopwords.words('english')]
        sentence_tokens.append(tokens_without_sw)
        for i in tokens_without_sw:
            unique_words.add(i)

    print(len(unique_words),"unique words")
    return list(unique_words),sentence_tokens

def one_hot_processing(words):
    one_hot={}
    word_index = {}
    for i,x in enumerate(words):
        vec=np.zeros(len(words))
        vec[i]=1
        one_hot[x]=vec
        word_index[x] = i
    return one_hot, word_index

def softmax(x):
    ex = np.exp(x - np.max(x))
    return ex / ex.sum()

def generate_train_data(sent_tokens, one_hot, window_size):

    X_train, y_train = [], []

    for sentence in sent_tokens:
        for i,w in enumerate(sentence):
            X_train.append(one_hot[w])
            context = np.zeros(one_hot[w].shape)
            for j in range(i-window_size, i+window_size + 1):
                if i!=j and j>=0 and j<len(sentence):
                    context += one_hot[sentence[j]]
            y_train.append(context)

    return X_train, y_train

def init_weights(num_words, num_hidden_layer):
    W = np.random.normal(size=(num_hidden_layer,num_words))
    W1 = np.random.normal(size=(num_words,num_hidden_layer))
    return W, W1

def train_skip_gram(one_hot, xs, ys, epochs, num_hidden_layer, learn):

    W, W1 =init_weights(len(one_hot),num_hidden_layer)

    for ep in range(epochs):
        if ep%100 == 0:
            print("\nEpoch", ep, end="..")
        if ep%5 == 0:
            print(".", end="", flush=True)
        for x, y in zip(xs, ys):

            #print("x", x.shape)
            #print("y", y.shape)

            out1 = W.dot(x)
            out2 = W1.dot(out1)
            z = softmax(out2)

            #print("out1", out1.shape)
            #print("z", z.shape)

            err = z - y

            #print("err", err.shape)

            #print("W",W.shape)
            #print("W1",W1.shape)

            gradW1 = np.asarray([err]).T @ np.asarray([out1])

            #print("gradW1",gradW1.shape)

            back_err = W1.T @ err

            #print("back_err",back_err.shape)

            gradW = np.asarray([back_err]).T @ np.asarray([x])

            #print("gradW",gradW.shape)

            W -= learn*gradW
            W1 -= learn*gradW1

    print("")
    return W, W1


def find_closest(word_vec, word, count = 5):

    current_word_vec = word_vec[word_index[word]]
    neighs = [(i, np.linalg.norm(current_word_vec-word_vec[i])) for i in range(len(word_vec))]

    neighs.sort(key=lambda n: n[1])

    return neighs[:count+1]


text = read("Lab8/water.txt")
unique_words, sentence_tokens = preprocess(text)
one_hot, word_index = one_hot_processing(unique_words)

Xs, Ys = generate_train_data(sentence_tokens,one_hot,window_size=4)

W, W1 = train_skip_gram(one_hot, Xs, Ys, epochs=400, num_hidden_layer=30, learn=1e-3)

word_vec = []

for i in range(len(unique_words)):
    word_vec.append(W[:, i])

aggl = AgglomerativeClustering(n_clusters=10)
clusters = aggl.fit_predict(word_vec)
print("aggl",clusters)

tsne = TSNE(n_components = 2)
vec_resized = tsne.fit_transform(word_vec)
print(vec_resized.shape)

plt.scatter(vec_resized[:,0],vec_resized[:,1],c=clusters)

for i in range(len(vec_resized)):
    plt.annotate(unique_words[i],(vec_resized[i,0],vec_resized[i,1]))

plt.show()

# print(word_vec)

for i,s in find_closest(word_vec, "cities"):
    print(unique_words[i],s)

classes = {}
for i,w in enumerate(unique_words):
    if clusters[i] in classes:
        classes[clusters[i]].append(w)
    else:
        classes[clusters[i]] = [w]

for k in classes.keys():
    print(k,classes[k])