#! /usr/bin/env python3

import argparse, psutil
from time import sleep

def get_cpu_utils(last_idle, last_total):
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = 1.0 - idle_delta / total_delta

parser = argparse.ArgumentParser(description='Generate stats on network and CPU utilization')

parser.add_argument('-b', required=True, help='IP/named address of the message broker')
parser.add_argument('-p', type=int, help='Virtual host (defaualt is "/")')
parser.add_argument('-c', type=int, help='login:password')
parser.add_argument('-k', type=int, required=True, help='routing key')

args = parser.parse_args()

bytes_sent = 0
bytes_received = 0

msg = {'net': {}, 'cpu_usage': 0}

while 1:
    msg['cpu_usage'] = psutil.cpu_percent(interval=1)
    network_io = psutil.net_io_counters(pernic=True)
    for nic in network_io:
        bytes_sent_old = bytes_sent
        bytes_received_old = bytes_received

        bytes_sent = network_io[nic].bytes_sent
        bytes_received = network_io[nic].bytes_recv

        tx_throughput = bytes_sent - bytes_sent_old
        rx_throughput = bytes_received - bytes_received_old

        msg['net'][nic] = {'tx': tx_throughput, 'rx': rx_throughput}

    print(msg)
