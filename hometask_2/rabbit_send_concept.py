#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Создаём обменник, по которому можно публиковать и принимать сообщения
# он принимает решение - в одну очередь или в несколько закидываем сообщения
# задаём тип посложнее - сообщение, отправленное с определенным ключом маршрутизации,
# будет доставлено во все очереди, связанные с соответствующим ключом привязки.
# Есть спецключи:
# - * (звездочка) может заменить ровно одно слово.
# - # (решетка) может заменить ноль или более слов.
# Когда очередь привязана с помощью ключа привязки "#" (хэш), она будет получать все сообщения, независимо от ключа маршрутизации, как при exchange fanout
# Когда в привязках не используются специальные символы «*» (звездочка) и «#» (решётка), обмен темами будет вести себя так же, как и exchange direct.
# Сообщение с ключом маршрутизации, установленным на «quick.orange.rabbit», будет доставлено в обе очереди.
# Сообщение "lazy.orange.elephant" также будет отправлено им обоим.
# С другой стороны, «quick.orange.fox» попадет только в первую очередь, а «lazy.brown.fox» — только во вторую.
# «lazy.pink.rabbit» будет доставлен во вторую очередь только один раз, даже если он соответствует двум привязкам.
# «quick.brown.fox» не соответствует ни одной привязке, поэтому она будет удалена.
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

#channel.queue_declare(queue='hello') # очереди будут заданы в обменнике на стороне ресивера

# And to emit a log with a routing key "kern.critical" type:

# python emit_log_topic.py "kern.critical" "A critical kernel error"
# routing_key = "kern.critical"
# message = "A critical kernel error"

#import sys
#routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
#message = ' '.join(sys.argv[2:]) or 'Hello World!' # В топик hello world не доставит, если не соответствует топик или выше не указать #
                                                    # сейчас настроен топик на "kern.critical"
#routing_key = "kern.critical"
routing_key = "kern.meow"
message = "A meow kernel error"

channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()