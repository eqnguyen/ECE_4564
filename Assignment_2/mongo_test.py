#! /usr/bin/env python3

import pymongo
import psutil
import datetime
import json
from pprint import pprint
from pymongo import MongoClient

print('Opening Mongo client')
client = MongoClient()
db = client.host_monitor_database
posts = db.posts

print('Deleting old entries')
posts.delete_many({})


def get_cpu_utils():
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)

    idle_delta = idle - get_cpu_utils.last_idle
    total_delta = total - get_cpu_utils.last_total

    get_cpu_utils.last_idle = idle
    get_cpu_utils.last_total = total

    utilisation = 1.0 - idle_delta / total_delta

    return utilisation


# simulates a static variable for get_cpu_utils
get_cpu_utils.last_idle, get_cpu_utils.last_total = 0, 0

while 1:
    msg = {'datetime': datetime.datetime.utcnow(), 'net': {}, 'cpu_usage': 0}

    # gets the cpu utilization, blocking, runs every second
    msg['cpu_usage'] = psutil.cpu_percent(interval=1)

    # gets the network info for each NIC
    network_io = psutil.net_io_counters(pernic=True)

    bytes_sent = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    bytes_received = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    bytes_sent_old = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    bytes_received_old = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    tx_throughput = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    rx_throughput = {'wlan0': 0, 'eth0': 0, 'lo': 0}

    for nic in network_io:
        bytes_sent_old[nic] = bytes_sent[nic]
        bytes_received_old[nic] = bytes_received[nic]

        bytes_sent[nic] = network_io[nic].bytes_sent
        bytes_received[nic] = network_io[nic].bytes_recv

        tx_throughput[nic] = bytes_sent[nic] - bytes_sent_old[nic]
        rx_throughput[nic] = bytes_received[nic] - bytes_received_old[nic]

        msg['net'][nic] = {'tx': tx_throughput[nic], 'rx': rx_throughput[nic]}

    posts.insert(msg)

    print('\nHost_1:')
    max_cpu = posts.find_one(sort=[('cpu_usage', -1)])['cpu_usage']
    min_cpu = posts.find_one(sort=[('cpu_usage', 1)])['cpu_usage']
    print('cpu: ' + str(msg['cpu_usage']) + '[Hi: ' + str(max_cpu) + ', Lo: ' + str(min_cpu) + ']')
    for item in msg['net']:
        print(
            item + ': rx=' + str(msg['net'][item]['rx']) + ' B/s [Hi:, Lo:], tx=' + str(
                msg['net'][item]['tx']) + ' B/s [Hi:, Lo:]')
