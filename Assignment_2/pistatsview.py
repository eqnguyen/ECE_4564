#! /usr/bin/env python3

import argparse
import pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', required=True, help='IP/named address of the message broker')
    parser.add_argument('-p', type=int, help='Virtual host (defaualt is "/")')
    parser.add_argument('-c', type=int, help='login:password')
    parser.add_argument('-k', type=int, required=True, help='routing key')

    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters(args.b))
    channel = connection.channel()

    channel.exchange_declare(exchange='pi_utilization', type='direct')

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

    if __name__ == "__main__":
        main()
