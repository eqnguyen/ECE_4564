#! /usr/bin/env python3

import asyncio
import pickle

from aiocoap import *

token = 1  # Player B
block_id = 57  # Diamond Block


async def main():
    protocol = await Context.create_client_context()

    # Get position from server
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

    # Check for valid token
    if tup[3] == token:
        # Payload format: (x, y, z, token, block_id)
        put_payload = (tup[0] + 1, tup[1], tup[2], token, block_id)
        print('\nPUT payload: %s' % (put_payload,))
        payload = pickle.dumps(put_payload)

        request = Message(code=PUT, payload=payload)
        request.opt.uri_host = '192.168.1.10'
        request.opt.uri_path = ('position',)

        response = await protocol.request(request).response

        print('PUT Minecraft player position')
        print('Result: %s\n%r\n' % (response.code, response.payload))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
