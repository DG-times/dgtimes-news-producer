import pika

HOST_NAME = "ec2-3-36-52-3.ap-northeast-2.compute.amazonaws.com"
QUEUE_NAME = "TEST_QUEUE"

class RabbitmqContextManager:
    """
    """
    def __init__(self):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST_NAME, port=5672,credentials=
                                                                        pika.PlainCredentials('guest', 'guest')))
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def __enter__(self):
        return self.channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
    
    def get_queue_name():
        return QUEUE_NAME