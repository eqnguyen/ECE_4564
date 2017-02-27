#! /usr/bin/env python3

import os, sys
import pymongo
from pymongo import MongoClient
from time import sleep

print('Opening Mongo client')
client = MongoClient()
db = client.host_monitor_database
posts = db.posts

while True:
    delete = input("Clear old data in the database? (Y/N): ").lower()
    if delete == 'y':
        print('Deleting old entries')
        posts.drop()
        break
    elif delete == 'n':
        break


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


# simulates a static variable for get_cpu_utils
get_cpu_util.last_idle, get_cpu_util.last_total = 0, 0

network_io = {}

prime_cpu_util()
prime_net_util(network_io)
sleep(1)

while 1:
    msg = {'net': {}, 'cpu': 0}

    # gets the cpu utilization, blocking, runs every second
    msg['cpu'] = get_cpu_util()
    # gets the network info for each NIC
    get_net_util(network_io)

    # calculate network throughput for each interface
    for nic in network_io:
        bytes_sent_old = network_io[nic]['bytes_tx_old']
        bytes_received_old = network_io[nic]['bytes_rx_old']

        bytes_sent = network_io[nic]['bytes_tx']
        bytes_received = network_io[nic]['bytes_rx']

        tx_throughput = bytes_sent - bytes_sent_old
        rx_throughput = bytes_received - bytes_received_old

        msg['net'][nic] = {'tx': tx_throughput, 'rx': rx_throughput}

    try:
        # post usage data to mongodb
        posts.insert(msg)

        # print statistics
        print('\nHost_1:')
        # get max and min cpu usage from mongo
        max_cpu = posts.find_one(sort=[('cpu', pymongo.DESCENDING)])['cpu']
        min_cpu = posts.find_one(sort=[('cpu', pymongo.ASCENDING)])['cpu']
        print('cpu: \t' + str(msg['cpu']) + ' [Hi: ' + str(max_cpu) + ', Lo: ' + str(min_cpu) + ']')
        for item in msg['net']:
            # get max and min rx/tx from mongo
            max_rx = posts.find_one(sort=[('net.' + item + '.rx', pymongo.DESCENDING)])['net'][item]['rx']
            min_rx = posts.find_one(sort=[('net.' + item + '.rx', pymongo.ASCENDING)])['net'][item]['rx']
            max_tx = posts.find_one(sort=[('net.' + item + '.tx', pymongo.DESCENDING)])['net'][item]['tx']
            min_tx = posts.find_one(sort=[('net.' + item + '.tx', pymongo.ASCENDING)])['net'][item]['tx']

            print(item + ':\trx=' + str(msg['net'][item]['rx']) + ' B/s ',
                  '[Hi: ' + str(max_rx) + ' B/s, Lo: ' + str(min_rx) + ' B/s], ',
                  'tx=' + str(msg['net'][item]['tx']) + ' B/s ',
                  '[Hi: ' + str(max_tx) + ' B/s, Lo: ' + str(min_tx) + ' B/s]')
    except Exception as e:
        print("Error: " + str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    sleep(1)
