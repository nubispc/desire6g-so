from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

class KafkaMessaging:
    def __init__(self, kafka_bootstrap_servers: str, input_topic: str, final_topic: str):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.input_topic = input_topic
        self.final_topic = final_topic
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_bootstrap_servers)
        self.consumer = KafkaConsumer(self.final_topic, bootstrap_servers=self.kafka_bootstrap_servers)

    async def send_message(self, message: bytes):
        try:
            future = self.producer.send(self.input_topic, message)
            record_metadata = future.get(timeout=10)
            print("Message sent successfully:", record_metadata)
        except KafkaError as e:
            print("Error sending message:", e)

    async def receive_message(self):
        try:
            for message in self.consumer:
                return message.value.decode()
        except KafkaError as e:
            print("Error receiving message:", e)
