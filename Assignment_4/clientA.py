#! /usr/bin/env python3

import asyncio
import logging
import pickle

from aiocoap import *

logging.basicConfig(level=logging.INFO)

token = 1


async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://192.168.1.10/position')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        tup = pickle.loads(response.payload)
        print('\nGET Minecraft player position')
        print('Result: %s\n%r' % (response.code, tup))

    
    context = await Context.create_client_context()

    await asyncio.sleep(2)

    tup = (1, 1, 1, token)
    payload = pickle.dumps(tup)

    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = '192.168.1.10'
    request.opt.uri_path = ('position',)

    response = await context.request(request).response

    print('\nPUT Minecraft player position')
    print('Result: %s\n%r' % (response.code, response.payload))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
