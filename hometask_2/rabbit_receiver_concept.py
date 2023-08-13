#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic') #
    # pika.exceptions.ChannelClosedByBroker: (406, "PRECONDITION_FAILED - inequivalent arg 'type' for exchange 'logs' in vhost '/': received 'topic' but current is 'fanout'")
    # надо было название обменника переименовать, был exchange='logs'
    
#    channel.queue_declare(queue='hello') # со стороны обменника зададим всё

    result = channel.queue_declare(queue='', exclusive=True) #стандартная пустая очередь, сервер придумает название; консьюмер закрылся - сворачиваем очередь
    queue_name = result.method.queue
    
#    binding_keys = sys.argv[1:]
#    if not binding_keys:
#        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
#        sys.exit(1)

    # To receive all the logs run:
#    binding_keys="#"
    # To receive all logs from the facility "kern":
#    binding_keys = "kern.*"
    # Or if you want to hear only about "critical" logs:
#    binding_keys ="*.critical"
    #You can create multiple bindings:
    binding_keys = ("kern.*", "*.critical")

    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)


    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)