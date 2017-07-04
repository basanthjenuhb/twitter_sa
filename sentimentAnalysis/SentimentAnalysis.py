import keras
import numpy as np
import pickle
import gensim, gc
from nltk.tokenize import TweetTokenizer
import emoji

class SentimentAnalysis:
    def __init__(self, modelFile, slangsFile, word2vecFile, vectorSize):
        self.model = keras.models.load_model(modelFile)
        self.slangs = pickle.load(open(slangsFile,'rb'))
        self.tweet_w2v = gensim.models.KeyedVectors.load_word2vec_format(word2vecFile, binary=True)
        self.vectorSize = vectorSize

    def tokenize(self, tweet):
        tweet = str(tweet).lower()
        tokens = TweetTokenizer().tokenize(tweet)
        tokens = [token for token in tokens if not (token.startswith("@") or token.startswith("http") or token.startswith("#"))]
        final_tokens = []
        for i in range(len(tokens)):
            try:
                tokens[i] = self.slangs[tokens[i]]
            except:
                continue
        for i in range(len(tokens)):
            try:
                words = emoji.UNICODE_EMOJI[tokens[i]][1:-1].split("_")
                final_tokens += words
            except:
                final_tokens.append(tokens[i])
        return final_tokens

    def wordvector(self, tokens):
        vec = np.zeros(self.vectorSize).reshape((1, self.vectorSize))
        count = 0.
        for word in tokens:
            try:
                vec += self.tweet_w2v[word].reshape((1, self.vectorSize))
                count += 1.
            except KeyError:
                continue
        if count != 0:
            vec /= count
        return vec

    def classify(self, scentence):
        print(self.model.predict(self.wordvector(self.tokenize(scentence))).argmax(axis = 1))

if __name__ == "__main__":
    modelFile = "../resources/model1.h5"
    slangsFile = "../resources/slangs.pkl"
    word2vecFile = "../resources/google.bin.gz"
    a = SentimentAnalysis(modelFile, slangsFile, word2vecFile)
    a.classify("Modi govt is doing a great job 😂😂😂😂😂😂")
    gc.collect()