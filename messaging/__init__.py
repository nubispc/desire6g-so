from .rabbitmq import RabbitMQMessaging
from .kafka import KafkaMessaging
from typing import Union

def get_messaging_system() -> Union[RabbitMQMessaging, KafkaMessaging]:
    messaging_system = os.getenv("MESSAGING_SYSTEM", "rabbitmq")

    if messaging_system == "rabbitmq":
        return RabbitMQMessaging(
            rabbitmq_host=os.getenv("RABBITMQ_HOST", "localhost"),
            input_topic=os.getenv("INPUT_TOPIC", "input_topic"),
            final_topic=os.getenv("FINAL_TOPIC", "final_topic")
        )
    elif messaging_system == "kafka":
        return KafkaMessaging(
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            input_topic=os.getenv("INPUT_TOPIC", "input_topic"),
            final_topic=os.getenv("FINAL_TOPIC", "final_topic")
        )
    else:
        raise ValueError("Invalid messaging system specified")
