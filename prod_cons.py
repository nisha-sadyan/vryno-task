import pika
import aio_pika
import json
import asyncio
from d_handeler import data


class producer_consumer:
    def __init__(self, process_callable, send_topic, receive_topic):
        self.async_connection = None
        self.send_topic = send_topic
        self.queue = ""
        self.receive_topic = receive_topic
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=self.queue)
        self.exchange = self.channel.exchange_declare(
            exchange=self.send_topic, exchange_type="topic"
        )
        self.process_callable = process_callable

    async def send(self, message: dict):
        self.channel.basic_publish(
            exchange="", routing_key=self.send_topic, body=json.dumps(message).encode('utf-8'))
        
        print("Published message:{}".format(message))
        # self.channel.basic_consume(queue=self.receive_topic, on_message_callback=self.process_callable)

        await self.connection.close()

    async def receive(self, loop):
        self.connection = await aio_pika.connect_robust(
            "amqp://guest:guest@localhost/", loop=loop
        )
        # async with self.connection:
        channel = await self.connection.channel()
        queue = await channel.declare_queue(self.receive_topic)
        await queue.consume(callback=self.process_incoming_message, no_ack=False)
        print("Established pika async listener")
        print("prod_cons")
        # await asyncio.Future()

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        print("incoming message", message)
        await message.ack()
        body = message.body
        # logger.info('Received message')
        if body:
            await self.process_callable(json.loads(body))
