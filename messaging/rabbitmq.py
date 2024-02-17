from aio_pika import connect, Message
from aio_pika.exceptions import QueueEmpty
import os
import asyncio

class RabbitMQMessaging:
    def __init__(self, rabbitmq_host: str, input_topic: str, final_topic: str):
        self.rabbitmq_host = rabbitmq_host
        self.input_topic = input_topic
        self.final_topic = final_topic
        self.channel = None
        self.connection = None

    async def connect(self):
        self.connection = await connect(f"amqp://{self.rabbitmq_host}/")
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.input_topic)
        await self.channel.declare_queue(self.final_topic)

    async def send_message(self, message: bytes):
        await self.channel.default_exchange.publish(
            Message(message),
            routing_key=self.input_topic
        )

    async def receive_message(self):
        queue = await self.channel.get_queue(self.final_topic)
        message = await queue.get(timeout=5)
        if message:
            await message.ack()
            return message.body.decode()
        else:
            return None
