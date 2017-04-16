#! /usr/bin/env python3

import psutil
import pickle
import sys

import rasdrive_classes as RASD

import asyncio
import aiocoap
import aiocoap.resource as resource


class StatusResource(resource.Resource):
    def __init__(self):
        super(StatusResource, self).__init__()
        get_RASD_Status()

    async def render_get(self, request):
        return aiocoap.Message(payload=pickle.dumps(get_RASD_Status()))


def get_RASD_Status():
    cpu_percent = psutil.cpu_percent(interval=0)
    network_io = psutil.net_io_counters(pernic=False)
    disk_usage = psutil.disk_usage('/').percent

    net_stats = RASD.RASD_Net_Load(bytes_sent=network_io.bytes_sent,
                                   bytes_recv=network_io.bytes_recv,
                                   errin=network_io.errin,
                                   errout=network_io.errout,
                                   dropin=network_io.dropin,
                                   dropout=network_io.dropout)

    return RASD.RASD_Status(cpu_percent=cpu_percent, net_stats=net_stats, disk_usage=disk_usage)


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('status',), StatusResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)
        print('Exiting program...')
        sys.exit(1)
