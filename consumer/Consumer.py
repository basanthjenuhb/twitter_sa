from kafka import KafkaConsumer
from sentimentAnalysis.SentimentAnalysis import SentimentAnalysis
from configurationLoader.ConfigurationLoader import ConfigurationLoader
import json
from elasticsearch import Elasticsearch
import time
import atexit

class Consumer:
    """
    Defines a consumer class.
    Takes 1 argument:
        * Path to configuration file
    Initialize:
        * Instance to Elasticsearch
        * Instance to kafkaconsumer
        * Instance to sentimentAnalysis classifier.
    """
    def __init__(self, configurationFile):
        self.elasticSearch = Elasticsearch()
        self.configuration = ConfigurationLoader(configurationFile)
        self.topic = self.configuration.getTopic()
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers = self.configuration.getBootstrapServers() )
        modelFile = self.configuration.getModelFile()
        slangsFile = self.configuration.getSlangsFile()
        word2vecFile = self.configuration.getword2vecFile()
        vectorSize = self.configuration.getVectorSize()
        self.model = SentimentAnalysis(modelFile, slangsFile, word2vecFile, vectorSize)
        atexit.register(self.close)

    def format(self, message):
        """
        Convert byte string to json.
        """
        return json.loads(message.decode('utf-8'))
    
    def elasticIndex(self, sentence, score):
        """
        Generates a JSON of the form
        {
            "tweet":"some tweet"
            "score": 2.3 # SOme score between -5 to +5
            "timeStamp": 23536463546 # Milliseconds from epoch
        }
        """
        tweetData = { 'tweet' : sentence,
                     'score' : score,
                     'timeStamp' : int(round(time.time() * 1000))
                   }
        self.elasticSearch.index(index = self.configuration.getIndex(),
                            doc_type = self.configuration.getDocType(),
                            body = tweetData)

    def stream(self):
        """
        Takes each message from kafkaConsumer.
        Classifies the message and Gives it a score.
        Sends the data to elasticIndex()
        """
        for message in self.consumer:
            sentence = self.format(message.value)['text']
            score = self.model.classify(sentence)
            self.elasticIndex(sentence, score)
            #print(score, sentence)
    
    def close(self):
        """
        Closes the consumer.
        """
        self.consumer.close()

if __name__ == "__main__":
    c = Consumer("resources/configurations.txt")
    c.stream()
