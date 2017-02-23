#! /usr/bin/env python3

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.exchange_declare(exchange='host_stats',
                         type='direct')

channel.basic_publish(exchange='host_stats',
                      routing_key='woah',
                      body='Hello World!')

channel.basic_publish(exchange='host_stats',
                      routing_key='first',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")
