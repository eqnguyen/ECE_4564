#! /usr/bin/env python3

import pika
import sys

if(len(sys.argv) >= 2):
	ip = sys.argv[1]
else:
	ip = 'localhost'

credentials = pika.PlainCredentials('rabbit_user', 'rabbit_pass')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    ip, 5672, 'rabbit_vhost', credentials))
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
