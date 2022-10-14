import pika

class rabbitmqconfigure():

    # configure rabbit mq server

    def __init__(self,queue="hello",host='localhost',routing_key='hello',exchange=''):
        self.queue=queue
        self.host=host
        self.routing_key= routing_key
        self.exchange= exchange

class Rabbitmq():
    def __init__(self,server1):
        
        # use composition instead of inheritance

        self.server1= server1
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server1.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server1.queue)
    def publish(self,payload={}):

        # pass the json payload

        self._channel.basic_publish(routing_key= self.server1.routing_key, exchange=self.server1.exchange,body=str(payload))
        print("Published message:{}".format(payload))
        self._connection.close()

if __name__=="__main__":
    server1= rabbitmqconfigure(queue="hello",host='localhost',routing_key='hello',exchange='')
    server= Rabbitmq(server1)
    server.publish(payload={"rabbit12":"Also so cute", "but":"little naughty12"})
