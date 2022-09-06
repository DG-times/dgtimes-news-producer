import time
from tool.RabbitmqContextManager import RabbitmqContextManager


def run(data:list, delay:float):
    with RabbitmqContextManager() as connection:
        for datum in data:
            connection.basic_publish(exchange='', routing_key=RabbitmqContextManager.get_queue_name(), body=datum)
            time.sleep(float(delay))
