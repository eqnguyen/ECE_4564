#! /usr/bin/env python3

import pika
import sys


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

if(len(sys.argv) >= 2):
        ip = sys.argv[1]
else:
        ip = 'localhost'

credentials = pika.PlainCredentials('rabbit_user', 'rabbit_pass')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    ip, 5672, 'rabbit_vhost', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='host_stats',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

routing_keys = ['first', 'second', 'third', 'woah']
for key in routing_keys:
    channel.queue_bind(exchange='host_stats',
                       queue=queue_name,
                       routing_key=key)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
