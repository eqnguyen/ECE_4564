#! /usr/bin/env python3

import pymongo
import psutil
from pprint import pprint
from pymongo import MongoClient

print('Opening Mongo client')
client = MongoClient()
db = client.host_monitor_database
posts = db.posts

print('Deleting old entries')
posts.drop()


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
    msg = {'net': {}, 'cpu_usage': 0}

    # gets the cpu utilization, blocking, runs every second
    msg['cpu_usage'] = psutil.cpu_percent(interval=1)

    # gets the network info for each NIC
    network_io = psutil.net_io_counters(pernic=True)

    # initialize dictionaries
    bytes_sent = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    bytes_received = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    bytes_sent_old = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    bytes_received_old = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    tx_throughput = {'wlan0': 0, 'eth0': 0, 'lo': 0}
    rx_throughput = {'wlan0': 0, 'eth0': 0, 'lo': 0}

    # calculate network throughput for each interface
    for nic in network_io:
        bytes_sent_old[nic] = bytes_sent[nic]
        bytes_received_old[nic] = bytes_received[nic]

        bytes_sent[nic] = network_io[nic].bytes_sent
        bytes_received[nic] = network_io[nic].bytes_recv

        tx_throughput[nic] = bytes_sent[nic] - bytes_sent_old[nic]
        rx_throughput[nic] = bytes_received[nic] - bytes_received_old[nic]

        msg['net'][nic] = {'tx': tx_throughput[nic], 'rx': rx_throughput[nic]}

    # post usage data to mongodb
    posts.insert(msg)

    # print statistics
    print('\nHost_1:')
    # get max and min cpu usage from mongo
    max_cpu = posts.find_one(sort=[('cpu_usage', pymongo.DESCENDING)])['cpu_usage']
    min_cpu = posts.find_one(sort=[('cpu_usage', pymongo.ASCENDING)])['cpu_usage']
    print('cpu: ' + str(msg['cpu_usage']) + '[Hi: ' + str(max_cpu) + ', Lo: ' + str(min_cpu) + ']')
    for item in msg['net']:
        # get max and min rx/tx from mongo
        max_rx = posts.find_one(sort=[('net.' + item + '.rx', pymongo.DESCENDING)])['net'][item]['rx']
        min_rx = posts.find_one(sort=[('net.' + item + '.rx', pymongo.ASCENDING)])['net'][item]['rx']
        max_tx = posts.find_one(sort=[('net.' + item + '.tx', pymongo.DESCENDING)])['net'][item]['tx']
        min_tx = posts.find_one(sort=[('net.' + item + '.tx', pymongo.ASCENDING)])['net'][item]['tx']

        print(item + ': rx=' + str(msg['net'][item]['rx']) + ' B/s ',
              '[Hi: ' + str(max_rx) + ' B/s, Lo: ' + str(min_rx) + ' B/s], ',
              'tx=' + str(msg['net'][item]['tx']) + ' B/s ',
              '[Hi: ' + str(max_tx) + ' B/s, Lo: ' + str(min_tx) + ' B/s]')
