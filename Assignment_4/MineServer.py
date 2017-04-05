#! /usr/bin/env python3

import asyncio
import datetime
import logging
import pickle

import aiocoap
import aiocoap.resource as resource


class PositionResource(resource.Resource):
    def __init__(self):
        super(PositionResource, self).__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.token = 1
        self.content = (self.x, self.y, self.z, self.token)

    async def render_get(self, request):
        return aiocoap.Message(payload=pickle.dumps(self.content))

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = pickle.loads(request.payload)
        payload = ("New payload: %r" % self.content).encode('utf8')
        return aiocoap.Message(payload=payload)


class TimeResource(resource.ObservableResource):
    def __init__(self):
        super(TimeResource, self).__init__()
        self.notify()

    def notify(self):
        self.updated_state()
        asyncio.get_event_loop().call_later(6, self.notify)

    def update_observation_count(self, count):
        if count:
            # not that it's actually implemented like that here -- unconditional updating works just as well
            print("Keeping the clock nearby to trigger observations")
        else:
            print("Stowing away the clock until someone asks again")

    async def render_get(self, request):
        payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)


# Logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('time',), TimeResource())

    root.add_resource(('position',), PositionResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
