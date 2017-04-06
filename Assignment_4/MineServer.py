#! /usr/bin/env python3

import asyncio
import pickle

import aiocoap
import aiocoap.resource as resource


class PositionResource(resource.Resource):
    def __init__(self):
        super(PositionResource, self).__init__()
        self.content = (0, 0, 0, 0)

    async def render_get(self, request):
        return aiocoap.Message(payload=pickle.dumps(self.content))

    async def render_put(self, request):
        # Payload format: (x, y, z, token, block_id)
        payload = pickle.loads(request.payload)

        token = (payload[3] + 1) % 3

        self.content = (payload[0], payload[1], payload[3], token)
        payload = ('New payload: %r' % (self.content,)).encode('utf8')
        return aiocoap.Message(payload=payload)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('position',), PositionResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
