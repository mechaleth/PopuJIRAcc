import pika
from pydantic import BaseModel

#TopicsList:
#           "user_data"
#           "roles"
#       "update"
#       "remove"
#       "insert"
#   "account"

class AuthData(BaseModel):
    id: int
    user_name: str
    role_id: int

class Roles(BaseModel):
    id: int
    role: str

class RabbitConnector:
    def __init__(self) -> None:
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    
    def __del__(self):
        self._connection.close()
        
    def get_connection(self):
        return self._connection
    

class RabbitSendManager:
    def __init__(self, connection) -> None:
        self._channel = connection.channel()

    
    def _data_push(self, exchange, routing_key, message):
        self._channel.exchange_declare(exchange=exchange, exchange_type='topic')
        self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    
        
    
    def insert_users_data(self, user_id: int, user_name: str, role_id: str):
        self._data_push(exchange="account", routing_key = "insert.user_data",
                        message = AuthData(id=user_id, user_name=user_name,role_id=role_id).model_dump())
    
    
    def update_users_data(self, user_id: int, user_name: str, role_id: str):
        self._data_push(exchange="account", routing_key = "update.user_data",
                        message = AuthData(id=user_id, user_name=user_name,role_id=role_id).model_dump())
    
    def remove_users_data(self, user_id: int):
        self._data_push(exchange="account", routing_key = "remove.user_data",
                        message = {"id": user_id})
    
    def insert_role_data(self, role_id: str, role_name: str):
        self._data_push(exchange="account", routing_key = "insert.role_data",
                        message = Roles(role_name=role_name,id=role_id).model_dump())
    
    
    def update_role_data(self, role_id: int, role_name: str):
        self._data_push(exchange="account", routing_key = "update.role_data",
                        message = Roles(role_name=role_name,id=role_id).model_dump())
    
    def remove_role_data(self, role_id: int):
        self._data_push(exchange="account", routing_key = "remove.role_data",
                        message = {"id": role_id})
       