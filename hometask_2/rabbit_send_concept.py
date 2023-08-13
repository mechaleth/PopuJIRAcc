#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Создаём обменник, по которому можно публиковать и принимать сообщения
# он принимает решение - в одну очередь или в несколько закидываем сообщения
# задаём простой тип - просто рассылает сообщения во все известные очереди
# есть ещё топик, но с этим не успею сейчас разобраться
channel.exchange_declare(exchange='logs', exchange_type='fanout')

#channel.queue_declare(queue='hello') # очереди будут заданы в обменнике на стороне ресивера

channel.basic_publish(exchange='logs', routing_key='', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()