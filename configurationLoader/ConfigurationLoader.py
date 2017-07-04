import configparser

class ConfigurationLoader:
    def __init__(self, fileName):
        self.parser = configparser.ConfigParser()
        self.parser.read(fileName)
    
    def getTopic(self):
        return self.parser.get('kafkaConsumer','topic')
    
    def getBootstrapServers(self):
        return [self.parser.get('kafkaConsumer','bootrap_servers')]
    
    def getModelFile(self):
        return self.parser.get('classifier','modelFile')
    
    def getSlangsFile(self):
        return self.parser.get('classifier','slangsFile')
    
    def getword2vecFile(self):
        return self.parser.get('classifier','word2vecFile')
    
    def getVectorSize(self):
        return int(self.parser.get('classifier','vectorSize'))