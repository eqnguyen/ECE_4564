#! /usr/bin/env python3

import argparse
import asyncio
import pickle
import sys

from aiocoap import *
from mcpi import block

token = 2  # Player C
block_id = block.STONE.id  # Stone


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address")
    args = parser.parse_args()

    protocol = await Context.create_client_context()

    while True:
        # Get position from server
        request = Message(code=GET, uri='coap://%s/position' % args.ip_address)

        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            tup = pickle.loads(response.payload)
            print('\nGET Minecraft player position')
            print('Result: %s\n%r' % (response.code, tup))

        # Check for valid token
        if tup[3] == token:
            # Payload format: (x, y, z, token, block_id)
            put_payload = (tup[0] + 1, tup[1], tup[2], token, block_id)
            print('\nPUT payload: %s' % (put_payload,))
            payload = pickle.dumps(put_payload)

            request = Message(code=PUT, payload=payload)
            request.opt.uri_host = args.ip_address
            request.opt.uri_path = ('position',)

            response = await protocol.request(request).response

            print('PUT Minecraft player position')
            print('Result: %s\n%r\n' % (response.code, response.payload))
        elif tup[3] == 3:
            print('Wall is complete')
            break


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except:
        print('Exiting program...')
        sys.exit(1)
