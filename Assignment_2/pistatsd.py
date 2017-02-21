#! /usr/bin/env python3

import argparse, psutil

parser = argparse.ArgumentParser(description='Generate stats on network and CPU utilization')

parser.add_argument('-b', required=True, help='IP/named address of the message broker')
parser.add_argument('-p', type=int, help='Virtual host (defaualt is "/")')
parser.add_argument('-c', type=int, help='login:password')
parser.add_argument('-k', type=int, required=True, help='routing key')

args = parser.parse_args()

bytes_sent = 0
bytes_received = 0

while 1:
    cpu_usage = psutil.cpu_percent(interval=1)
    network_io = psutil.net_io_counters(pernic=True)
    for nic in network_io:
        bytes_sent_old = bytes_sent
        bytes_received_old = bytes_received

        bytes_sent = network_io[nic].bytes_sent
        bytes_received = network_io[nic].bytes_recv

        tx_throughput = bytes_sent - bytes_sent_old
        rx_throughput = bytes_received - bytes_received_old

        print(nic, tx_throughput, rx_throughput)
