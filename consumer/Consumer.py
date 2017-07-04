from kafka import KafkaConsumer
from sentimentAnalysis.SentimentAnalysis import SentimentAnalysis
from configurationLoader.ConfigurationLoader import ConfigurationLoader
import json

class Consumer:
    def __init__(self, configurationFile):
        configuration = ConfigurationLoader(configurationFile)
        self.topic = configuration.getTopic()
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers = configuration.getBootstrapServers() )
        modelFile = configuration.getModelFile()
        slangsFile = configuration.getSlangsFile()
        word2vecFile = configuration.getword2vecFile()
        vectorSize = configuration.getVectorSize()
        self.model = SentimentAnalysis(modelFile, slangsFile, word2vecFile, vectorSize)

    def format(self, message):
        return json.loads(message.decode('utf-8'))

    def stream(self):
        for message in self.consumer:
            sentence = self.format(message.value)['text']
            self.model.classify(sentence)

if __name__ == "__main__":
    c = Consumer("resources/configurations.txt")
    c.stream()
