from kafka import KafkaConsumer
from S\
import json

class Consumer:
    def __init__(self, topic):
        self.topic = topic
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=['localhost:9092'])
        self.queue = []
        # model = ke

    def format(self, message):
        return json.dumps(message.decode('utf-8'))

    def stream(self):
        for message in self.consumer:
            print(self.format(message.value))

if __name__ == "__main__":
    c = Consumer("twitter_stream")
    c.stream()
