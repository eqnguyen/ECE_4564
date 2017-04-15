#! /usr/bin/env python3

import argparse
import asyncio
import pickle
import sys

from aiocoap import *


async def main():
    protocol = await Context.create_client_context()

    while True:
        # Get position from server
        request = Message(code=GET, uri='coap://%s/status' % 'localhost')

        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            tup = pickle.loads(response.payload)
            print('\nGET CPU/Network/Disk status')
            print('Result: %s\n%r' % (response.code, tup))

