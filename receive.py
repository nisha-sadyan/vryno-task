import pika, sys, os

class rabbitmqserverconfigure():
    # server initialization
    def __init__(self,queue='hello',host='localhost'):
        self.queue=queue
        self.host=host
    

class rabbitmqserver():
    def __init__(self,server):
        self.server=server
        self.server._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self.server._channel = self.server._connection.channel()
        self._temp=self.server._channel.queue_declare(queue=self.server.queue)

    def callback(ch, method, properties, body):
        print(" [x] Received %s" % body)

    def startserver(self):
        self._channel.basic_consume(queue=self.server.queue, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()

if __name__ == '__main__':
    serverconfig= rabbitmqserverconfigure()
    server = rabbitmqserver(server=serverconfig)
    server.startserver()