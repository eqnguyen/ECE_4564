#! /usr/bin/env python3

import asyncio
import pickle
import sys

import aiocoap
import aiocoap.resource as resource
from mcpi.minecraft import Minecraft

import RPi.GPIO as GPIO

mc = Minecraft.create()


class PositionResource(resource.Resource):
    def __init__(self):
        super(PositionResource, self).__init__()
        self.init_pos = mc.player.getTilePos()
        print('Initial position:', self.init_pos.x, self.init_pos.y, self.init_pos.z)
        self.content = (self.init_pos.x, self.init_pos.y, self.init_pos.z, 0)

    async def render_get(self, request):
        pos = mc.player.getTilePos()

        # Check if wall is complete
        if pos.x == self.init_pos.x + 10 and pos.y == self.init_pos.y + 1 and pos.z == self.init_pos.z:
            token = 3
            GPIO.output(chan_list, (False, False, False))
            print('Wall is complete')
            mc.postToChat('Wall is complete')
        else:
            token = self.content[3]

        self.content = (pos.x, pos.y, pos.z, token)
        return aiocoap.Message(payload=pickle.dumps(self.content))

    async def render_put(self, request):
        # Payload format: (x, y, z, token, block_id)
        payload = pickle.loads(request.payload)

        # Update player position (x, y, z)
        mc.player.setTilePos(payload[0], payload[1], payload[2])

        # Set block at payload location with block_id
        mc.setBlock(payload[0], payload[1], payload[2], payload[4])

        # Set token for next player
        token = (payload[3] + 1) % 3

        # Change LED color to indicate which client's turn it is
        GPIO.output(chan_list, (token == 0, token == 1, token == 2))

        # Send PUT response
        self.content = (payload[0], payload[1], payload[2], token)
        payload = ('Block set at: %r' % (self.content,)).encode('utf8')
        print(payload)
        return aiocoap.Message(payload=payload)


def main():
    # Set pin mode to the numbers you can read off the pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up channel list
    global chan_list
    chan_list = [13, 19, 26]  # 13 red, 19 green, 26 blue
    GPIO.setup(chan_list, GPIO.OUT)

    # Resource tree creation
    root = resource.Site()

    root.add_resource(('position',), PositionResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    try:
        main()
    except:
        print('Exiting program...')
        GPIO.cleanup(chan_list)
        sys.exit(0)
