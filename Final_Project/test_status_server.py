#! /usr/bin/env python3

# This script tests status_server.py by making CoAP requests to the server

# Instructions:
# First run status_server.py then run this script to get status updates
# from the Pi

import asyncio
import pickle
import sys

from aiocoap import *
from time import sleep


async def main():
    protocol = await Context.create_client_context()

    while True:
        # Get position from server
        request = Message(code=GET, uri='coap://{hostname}/status'.format(hostname='localhost'))

        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            tup = pickle.loads(response.payload)
            print('\nGET CPU/Network/Disk status')
            print('Result: %s\n%s' % (response.code, tup))

        sleep(1)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except:
        print('Exiting program...')
        sys.exit(1)
