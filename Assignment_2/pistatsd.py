#! /usr/bin/env python3

import argparse
from time import sleep
import pika
import json


def get_cpu_util():
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)

    idle_delta = idle - get_cpu_util.last_idle
    total_delta = total - get_cpu_util.last_total

    get_cpu_util.last_idle = idle
    get_cpu_util.last_total = total

    utilisation = 1.0 - idle_delta / total_delta

    return utilisation


def prime_cpu_util():
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)

    get_cpu_util.last_idle = idle
    get_cpu_util.last_total = total


def get_net_util(devices):
    with open('/proc/net/dev') as f:
        dev = f.read()
    dev = dev.split('\n')[2:]

    for device_stats in dev:
        if device_stats == '':
            continue
        device = device_stats.split(':')[0].strip()
        if device in devices:
            devices[device]['bytes_tx_old'] = devices[device]['bytes_tx']
            devices[device]['bytes_rx_old'] = devices[device]['bytes_rx']
            devices[device]['bytes_tx'] = int(device_stats.split()[9])
            devices[device]['bytes_rx'] = int(device_stats.split()[1])
        else:
            devices[device] = {'bytes_tx_old': 0, 'bytes_rx_old': 0, 'bytes_tx': 0, 'bytes_rx': 0, }

            devices[device]['bytes_tx_old'] = int(device_stats.split()[9])
            devices[device]['bytes_rx_old'] = int(device_stats.split()[1])
            devices[device]['bytes_tx'] = int(device_stats.split()[9])
            devices[device]['bytes_rx'] = int(device_stats.split()[1])


def prime_net_util(devices):
    with open('/proc/net/dev') as f:
        dev = f.read()
    dev = dev.split('\n')[2:]

    for device_stats in dev:
        if device_stats == '':
            continue
        device = device_stats.split(':')[0].strip()
        devices[device] = {'bytes_tx_old': 0, 'bytes_rx_old': 0, 'bytes_tx': 0, 'bytes_rx': 0, }

        devices[device]['bytes_tx'] = int(device_stats.split()[9])
        devices[device]['bytes_rx'] = int(device_stats.split()[1])


# -------------------- Parsing command line ------------------------------------------
parser = argparse.ArgumentParser(description='Publishes stats on network and CPU utilization to a RabbitMQ broker')

parser.add_argument('-b', required=True, help='IP/named address of the message broker')
parser.add_argument('-p', help='Virtual host (default is "/")')
parser.add_argument('-c', help='login:password')
parser.add_argument('-k', required=True, help='routing key')

args = parser.parse_args()
if args.p is None:
    args.p = '/'
if args.c is None:
    args.c = 'guest:guest'
temp = args.c.split(':', 2)
user = temp[0]
password = temp[1]
# ------------------------------------------------------------------------------------

# ---------- set up connection and queue with rabbitMQ broker ------------------------
#credentials = pika.PlainCredentials(user, password)
#connection = pika.BlockingConnection(pika.ConnectionParameters(
#    args.b, 5672, args.p, credentials))
#channel = connection.channel()

#channel.exchange_declare(exchange='pi_utilization',
#                         type='direct')
# ------------------------------------------------------------------------------------

bytes_sent, bytes_received = 0, 0
# simulates a static variable for get_cpu_utils
get_cpu_util.last_idle, get_cpu_util.last_total = 0, 0
network_io = {}

prime_cpu_util()
prime_net_util(network_io)
sleep(1)

msg = {'net': {}, 'cpu': 0}

while 1:
    # gets the cpu utilization, blocking, runs every second
    msg['cpu'] = get_cpu_util()
    # gets the network info for each NIC
    get_net_util(network_io)
    for nic in network_io:
        bytes_sent_old = network_io[nic]['bytes_tx_old']
        bytes_received_old = network_io[nic]['bytes_rx_old']

        bytes_sent = network_io[nic]['bytes_tx']
        bytes_received = network_io[nic]['bytes_rx']

        tx_throughput = bytes_sent - bytes_sent_old
        rx_throughput = bytes_received - bytes_received_old

        msg['net'][nic] = {'tx': tx_throughput, 'rx': rx_throughput}

    # publish the stats to a rabbitMQ server
#    channel.basic_publish(exchange='pi_utilization',
 #                         routing_key=args.k,
  #                        body=json.dumps(msg))
    print(msg)
    sleep(1)
