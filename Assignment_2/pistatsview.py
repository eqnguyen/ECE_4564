#! /usr/bin/env python3

import argparse, pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Publishes stats on network and CPU utilization to a RabbitMQ broker')

    # Add arguments to the parser
    parser.add_argument('-b', required=True, help='IP/named address of the message broker')
    parser.add_argument('-p', type=int, help='Virtual host (default is "/")')
    parser.add_argument('-c', type=int, help='login:password')
    parser.add_argument('-k', required=True, help='routing key')

    # Store arguments into variable
    args = parser.parse_args()

    # Create connection with rabbitMQ broker
    credentials = pika.PlainCredentials('rabbit_user', 'rabbit_pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        args.b, 5672, 'rabbit_vhost', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='pi_utilization', type='direct')
    result = channel.queue_declare(exclusive=True)

    queue_name = result.method.queue

    channel.queue_bind(exchange='pi_utilization', queue=queue_name, routing_key=args.k)
    channel.basic_consume(callback, queue=queue_name, no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Start consuming messages
    channel.start_consuming()


if __name__ == "__main__":
    main()
