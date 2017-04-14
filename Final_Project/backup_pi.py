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
        cpu_percent = psutil.cpu_percent(interval=0)
        network_io = psutil.net_io_counters(pernic=False)

        net_stats = RASD.RASD_Net_Load(bytes_sent=network_io.bytes_sent,
                                       bytes_recv=network_io.bytes_recv,
                                       errin=network_io.errin,
                                       errout=network_io.errout,
                                       dropin=network_io.dropin,
                                       dropout=network_io.dropout)

        self.status = RASD.RASD_Status(cpu_percent=cpu_percent, net_stats=net_stats)

    async def render_get(self, request):
        cpu_percent = psutil.cpu_percent(interval=0)
        network_io = psutil.net_io_counters(pernic=False)

        net_stats = RASD.RASD_Net_Load(bytes_sent=network_io.bytes_sent,
                                       bytes_recv=network_io.bytes_recv,
                                       errin=network_io.errin,
                                       errout=network_io.errout,
                                       dropin=network_io.dropin,
                                       dropout=network_io.dropout)

        self.status = RASD.RASD_Status(cpu_percent=cpu_percent, net_stats=net_stats)
        return aiocoap.Message(payload=pickle.dumps(self.status))


def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('status',), StatusResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    try:
        main()
    except:
        print('Exiting program...')
        sys.exit(1)
