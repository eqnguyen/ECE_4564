#! /usr/bin/env python3

import asyncio
import pickle

import aiocoap
import aiocoap.resource as resource
from mcpi.minecraft import Minecraft

mc = Minecraft.create()


class PositionResource(resource.Resource):
    def __init__(self):
        super(PositionResource, self).__init__()
        self.init_pos = mc.player.getPos()
        self.content = (self.init_pos.x, self.init_pos.y, self.init_pos.z, 0)

    async def render_get(self, request):
        pos = mc.player.getPos()
        self.content = (pos.x, pos.y, pos.z, self.content[3])

        if pos == (self.init_pos.x + 10, self.init_pos.y + 1, self.init_pos.z):
            payload = ('Complete',)
            return aiocoap.Message(payload=pickle.dumps(payload))
        else:
            return aiocoap.Message(payload=pickle.dumps(self.content))

    async def render_put(self, request):
        # Payload format: (x, y, z, token, block_id)
        payload = pickle.loads(request.payload)

        # Update player position
        mc.player.setPos(payload[0], payload[1], payload[2])

        # Set block at payload location with block_id
        mc.setBlock(payload[0], payload[1], payload[2], payload[4])

        # Set token for next player
        token = (payload[3] + 1) % 3

        # Send PUT response
        self.content = (payload[0], payload[1], payload[3], token)
        payload = ('Block set: %r' % (self.content,)).encode('utf8')
        return aiocoap.Message(payload=payload)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('position',), PositionResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
