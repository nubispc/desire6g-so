import os
import asyncio
from aio_pika import connect_robust, Message
from aio_pika.exceptions import QueueEmpty, AMQPConnectionError

class RabbitMQMessaging:
    def __init__(self, rabbitmq_host: str, input_topic: str, final_topic: str, max_retries: int):
        self.rabbitmq_host = rabbitmq_host
        self.input_topic = input_topic
        self.final_topic = final_topic
        self.channel = None
        self.connection = None
        self.max_retries = max_retries

    async def connect(self):
        try:
            self.connection = await connect_robust(f"amqp://{self.rabbitmq_host}/")
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.input_topic)
            await self.channel.declare_queue(self.final_topic)
        except AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")

    async def send_message(self, message: bytes):
        try:
            if self.channel is None or self.connection is None:
                await self.connect()

            await self.channel.default_exchange.publish(
                Message(message),
                routing_key=self.input_topic
            )
        except AMQPConnectionError as e:
            print(f"Error sending message: {e}")

    async def receive_message(self):
        try:
            if self.channel is None or self.connection is None:
                await self.connect()

            queue = await self.channel.get_queue(self.final_topic)
            for _ in range(self.max_retries):
                try:
                    message = await queue.get(timeout=3)
                    if message:
                        await message.ack()
                        return message.body.decode()
                except QueueEmpty:
                    print("No message yet available in the queue.")
                    await asyncio.sleep(3)  # Wait for 3 seconds before retrying
            print("No message available after retrying.")
            return None
        except AMQPConnectionError as e:
            print(f"Error receiving message: {e}")
