#! /usr/bin/env python3

import psutil

import asyncio
import aiocoap
import aiocoap.resource as resource

class StatusResource(resource.Resource):
    def __init__(self):
        super(StatusResource, self).__init__()

    async def render_get(self, request):

        cpu_usage = psutil.cpu_percent(interval=0)
        network_io = psutil.net_io_counters(pernic=False)


        self.content = (pos.x, pos.y, pos.z, token)
        return aiocoap.Message(payload=pickle.dumps(self.content))


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
        sys.exit(1)