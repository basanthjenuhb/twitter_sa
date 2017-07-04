import keras
import numpy as np
import pickle
import gensim

class SentimentAnalysis:
    def __init__(self, modelFile, slangsFile, word2vecFile):
        self.model = keras.models.load_model(modelFile)
        self.slangs = pickle.load(open(slangsFile,'rb'))
        self.tweet_w2v = gensim.models.KeyedVectors.load_word2vec_format(word2vecFile, binary=True)

    def tokenize(self, tweet):
        try:
            tweet = str(tweet).lower()
            tokens = tokenizer.tokenize(tweet)
            tokens = [token for token in tokens if
                      not (token.startswith("@") or token.startswith("http") or token.startswith("#"))]
            final_tokens = []
            for i in range(len(tokens)):
                try:
                    tokens[i] = slangs[tokens[i]]
                except:
                    continue
            for i in range(len(tokens)):
                try:
                    words = emoji.UNICODE_EMOJI[tokens[i]][1:-1].split("_")
                    final_tokens += words
                except:
                    final_tokens.append(tokens[i])
            return final_tokens
        except:
            return None

    def wordvector(self, tokens, size):
        vec = np.zeros(size).reshape((1, size))
        count = 0.
        for word in tokens:
            try:
                vec += self.tweet_w2v[word].reshape((1, size))
                count += 1.
            except KeyError:
                continue
        if count != 0:
            vec /= count
        return vec

    def classify(self, scentence):
        print(self.model.predict(self.wordvector(self.wordvector(scentence,300))))

if __name__ == "__main__":
    modelFile = "../resources/model1.h5"
    slangsFile = "../resources/slangs.pkl"
    word2vecFile = "../resources/google.bin.gz"
    a = SentimentAnalysis(modelFile, slangsFile, word2vecFile)