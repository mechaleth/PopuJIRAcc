import pika
from pydantic import BaseModel
from rabbit_send_concept import message

#TopicsList:
#           "user_data"
#           "roles"
#       "update"
#       "remove"
#       "insert"
#   "account"

class RabbitConnector:
    def __init__(self) -> None:
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    
    def __del__(self):
        self._connection.close()
        
    def get_connection(self):
        return self._connection

class RabbitSendManager:
    def __init__(self, connection) -> None:
        self._connection = connection
        self._channel = connection.channel()
        result = self._channel.queue_declare(queue='', exclusive=True) #стандартная пустая очередь, сервер придумает название; консьюмер закрылся - сворачиваем очередь
        queue_name = result.method.queue
        binding_keys = ("account.*",)

        for binding_key in binding_keys:
            self._channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)


    
    def _data_get(self, exchange, routing_key, message):

        channel.exchange_declare(exchange=exchange, exchange_type='topic')
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    
    def 