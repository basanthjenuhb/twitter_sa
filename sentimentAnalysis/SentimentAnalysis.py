import keras
import numpy as np
import pickle
import gensim, gc
from nltk.tokenize import TweetTokenizer
import emoji

class SentimentAnalysis:
    """
    takes arguments:
        * path to keras Model file
        * path to slangs file
        * path to word2vec file
        * Vectorsize of each word
    Initialize:
        * Keras model
        * Slangs Disctionary
        * Google word2vec file
        * Vectorsize for each word
    """
    def __init__(self, modelFile, slangsFile, word2vecFile, vectorSize):
        self.model = keras.models.load_model(modelFile)
        self.slangs = pickle.load(open(slangsFile,'rb'))
        self.tweet_w2v = gensim.models.KeyedVectors.load_word2vec_format(word2vecFile, binary=True)
        self.vectorSize = vectorSize

    def tokenize(self, tweet):
    """
    1. Tokenize the tweets
    2. Remove the words with Hyperlinks, '#' or '@'
    3. Convert slangs to actual words using the slangs dictionary
    4. Convert emojis to their corresponging meanings
    """
        tweet = str(tweet).lower()
        tokens = TweetTokenizer().tokenize(tweet)
        tokens = [token for token in tokens if not (token.startswith("@") or token.startswith("http") or token.startswith("#"))]
        final_tokens = []
        for i in range(len(tokens)):
            try:
                tokens[i] = self.slangs[tokens[i]]
            except KeyError:
                continue
        for i in range(len(tokens)):
            try:
                words = emoji.UNICODE_EMOJI[tokens[i]][1:-1].split("_")
                final_tokens += words
            except KeyError:
                final_tokens.append(tokens[i])
        return final_tokens

    def wordvector(self, tokens):
    """
    Generate a vector for each word in tweet from google word2vec
    Add all vectors and take average.
    """
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
    
    def getScore(self, score):
    """
    return a score between -5 to +5
    """
        return (score - 0.5) * 10

    def classify(self, scentence):
    """
    Get prediction from model and return score of tweet
    """
        scores = self.model.predict(self.wordvector(self.tokenize(scentence)))
        return self.getScore(scores[0][1])

if __name__ == "__main__":
    modelFile = "../resources/model1.h5"
    slangsFile = "../resources/slangs.pkl"
    word2vecFile = "../resources/google.bin.gz"
    a = SentimentAnalysis(modelFile, slangsFile, word2vecFile, 300)
    a.classify("Modi is an outlier")
    gc.collect()