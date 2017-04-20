#! /usr/bin/env python3

# This script makes CoAP requests to all nodes in the RasDrive network to determine
# system status

# Needs to run in conjunction with web_server.py to update the web server
# with system statuses

import asyncio
import pickle
import sys
from time import sleep

import rasdrive_classes as RASD
import requests
from aiocoap import *


async def checkStatus():
    # List of servers and backups on RasDrive network
    # Static lists for now but potentially dynamic in the future
    server_list = [RASD.RASD_Server('rasdserver1'), RASD.RASD_Server('rasdserver2')]
    backup_list = [RASD.RASD_Backup('rasdbackup1'), RASD.RASD_Backup('rasdbackup2')]

    protocol = await Context.create_client_context()
    s = requests.Session()

    while True:
        # Get statuses from all nodes on RasDrive network
        for node in server_list + backup_list:
            request = Message(code=GET, uri='coap://{hostname}.local/status'.format(hostname=node.hostname))

            try:
                response = await protocol.request(request).response
            except:
                # presumably server went offline...deal with it here
                print('Failed to fetch resource from:', node.hostname)
                node.status = None
            else:
                tup = pickle.loads(response.payload)
                print(tup)
                node.status = tup

        # Post list of RasDrive nodes with updated statuses to web server every 10 seconds
        payload = pickle.dumps({"server_list": server_list, "backup_list": backup_list})
        s.post("http://localhost:8888/com", data=payload)
        sleep(10)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(checkStatus())
        loop.close()
    except:
        print('Exiting program...')
        sys.exit(1)
