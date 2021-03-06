#! /usr/bin/env python3

# This script makes CoAP requests to all nodes in the RasDrive network to determine
# system status

# Needs to run in conjunction with web_server.py to update the web server
# with system statuses

import asyncio
import pickle
import socket
import sys
from time import sleep

import rasdrive_classes as RASD
import requests
from aiocoap import *


def get_ip(hostname):
    return socket.gethostbyname(hostname)


server_list = [RASD.RASD_Server('rasdserver1'), RASD.RASD_Server('rasdserver2')]
backup_list = [RASD.RASD_Backup('rasdbackup1'), RASD.RASD_Backup('rasdbackup2')]


async def checkStatus(list, index):
    global server_list
    global backup_list

    protocol = await Context.create_client_context()
    node = list[index]

    # Get statuses from all nodes on RasDrive network
    request = Message(code=GET, uri='coap://{hostname}.local/status'.format(hostname=node.hostname))

    try:
        response = await protocol.request(request).response
        ip = get_ip('{hostname}.local'.format(hostname=node.hostname))
        node.ip = ip
    except:
        # presumably server went offline...deal with it here
        print('Failed to fetch resource from:', node.hostname)
        node.ip = None
        node.status = None
    else:
        tup = pickle.loads(response.payload)
        print(tup)
        node.status = tup

    list[index] = node


def main():
    global server_list
    global backup_list

    s = requests.Session()
    loop = asyncio.get_event_loop()

    while True:
        tasks = [
            asyncio.ensure_future(checkStatus(server_list, 0)),
            asyncio.ensure_future(checkStatus(server_list, 1)),
            asyncio.ensure_future(checkStatus(backup_list, 0)),
            asyncio.ensure_future(checkStatus(backup_list, 1))
        ]

        loop.run_until_complete(asyncio.gather(*tasks))

        # Post list of RasDrive nodes with updated statuses to web server every 5 seconds
        payload = pickle.dumps({"server_list": server_list, "backup_list": backup_list})

        try:
            s.post("http://localhost:8888/com/status", data=payload)
        except:
            print('Could not post status to server')

        sleep(5)


if __name__ == "__main__":
    try:
        main()
    except:
        print('Exiting program...')
        sys.exit(1)
