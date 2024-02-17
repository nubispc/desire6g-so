from kafka import KafkaProducer, KafkaConsumer
import os

class KafkaMessaging:
    def __init__(self, kafka_bootstrap_servers: str, input_topic: str, final_topic: str):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.input_topic = input_topic
        self.final_topic = final_topic
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_bootstrap_servers)
        self.consumer = KafkaConsumer(self.final_topic, bootstrap_servers=self.kafka_bootstrap_servers)

    async def send_message(self, message: bytes):
        self.producer.send(self.input_topic, message)

    async def receive_message(self):
        for message in self.consumer:
            return message.value.decode()
