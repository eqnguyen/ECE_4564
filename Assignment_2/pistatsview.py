#! /usr/bin/env python3

import sys, argparse
import pika, pymongo
import json
import RPi.GPIO as GPIO
from pymongo import MongoClient
from pika.exceptions import (ConnectionClosed)

try:
    print('Opening Mongo client')
    client = MongoClient()
    db = client.host_monitor_database
    posts = db.posts
except Exception as e:
    print("Error: " + str(e))
    sys.exit(0)

while True:
    delete = input("Clear old data in the database? (Y/N): ").lower()
    if delete == 'y':
        print('Deleting old entries')
        client.drop_database("host_monitor_database")
        break
    elif delete == 'n':
        break

# set pin mode to the numbers you can read off the pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set up channel list
chan_list = [13, 19, 26]  # 13 red, 19 green, 26 blue
GPIO.setup(chan_list, GPIO.OUT)


def callback(ch, method, properties, body):
    data = json.loads(body.decode())

    try:
        # post usage data to MongoDB
        posts.insert(data)
    except:
        print("Error: Could not post to MongoDB")

    input = data['cpu']

    # Display LED based on threshold and input
    if input < .25:
        GPIO.output(chan_list, (False, True, False))  # green
    elif input < .5:
        GPIO.output(chan_list, (True, True, False))  # yellow
    else:
        GPIO.output(chan_list, (True, False, False))  # red

    print('\n%r' % method.routing_key)

    # get max and min cpu usage from Mongo
    max_cpu = posts.find_one(sort=[('cpu', pymongo.DESCENDING)])['cpu']
    min_cpu = posts.find_one(sort=[('cpu', pymongo.ASCENDING)])['cpu']
    print('cpu: \t' + str(data['cpu']) + ' [Hi: ' + str(max_cpu) + ', Lo: ' + str(min_cpu) + ']')
    for item in data['net']:
        # get max and min rx/tx from Mongo
        max_rx = posts.find_one(sort=[('net.' + item + '.rx', pymongo.DESCENDING)])['net'][item]['rx']
        min_rx = posts.find_one(sort=[('net.' + item + '.rx', pymongo.ASCENDING)])['net'][item]['rx']
        max_tx = posts.find_one(sort=[('net.' + item + '.tx', pymongo.DESCENDING)])['net'][item]['tx']
        min_tx = posts.find_one(sort=[('net.' + item + '.tx', pymongo.ASCENDING)])['net'][item]['tx']

        print(item + ':\trx=' + str(data['net'][item]['rx']) + ' B/s ',
              '[Hi: ' + str(max_rx) + ' B/s, Lo: ' + str(min_rx) + ' B/s], ',
              'tx=' + str(data['net'][item]['tx']) + ' B/s ',
              '[Hi: ' + str(max_tx) + ' B/s, Lo: ' + str(min_tx) + ' B/s]')


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Publishes stats on network and CPU utilization to a RabbitMQ broker')

    # Add arguments to the parser
    parser.add_argument('-b', required=True, help='IP/named address of the message broker')
    parser.add_argument('-p', help='Virtual host (default is "/")')
    parser.add_argument('-c', help='login:password')
    parser.add_argument('-k', required=True, help='routing key')

    # Store arguments into variable
    args = parser.parse_args()
    args = parser.parse_args()
    if args.p is None:
        args.p = '/'
    if args.c is None:
        args.c = 'guest:guest'
    temp = args.c.split(':')
    if(len(temp)< 2):
        print("Error: credentials must include a :")
        sys.exit(1)
    user = temp[0]
    password = temp[1]

    # Create connection with rabbitMQ broker
    try:
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            args.b, 5672, args.p, credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange='pi_utilization', type='direct')
        result = channel.queue_declare(exclusive=True)

        queue_name = result.method.queue

        channel.queue_bind(exchange='pi_utilization', queue=queue_name, routing_key=args.k)
        channel.basic_consume(callback, queue=queue_name, no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        # Start consuming messages
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        print("Error: pika connection closed")
        sys.exit(1)
    except pika.exceptions.ProbableAuthenticationError:
        print("Error: pika probable authentication error")
        sys.exit(1)
    except pika.exceptions.ProbableAccessDeniedError:
        print("Error: pika probably access denied error")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except:
        print('')
        GPIO.cleanup(chan_list)
        sys.exit(1)
