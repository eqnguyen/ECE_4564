#! /usr/bin/env python3

import asyncio
import pickle
import sys

import RPi.GPIO as GPIO
import aiocoap
import aiocoap.resource as resource
import psutil
import rasdrive_classes as RASD


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

    # Change LED to indicate current status of the system
    if cpu_percent < 25 and disk_usage < 50:
        GPIO.output(chan_list, (False, True, False))
    elif cpu_percent < 50 and disk_usage < 75:
        GPIO.output(chan_list, (True, True, False))
    else:
        GPIO.output(chan_list, (True, False, False))

    return RASD.RASD_Status(cpu_percent=cpu_percent, net_stats=net_stats, disk_usage=disk_usage)


def main():
    # Set ping mode to the numbers you can read off the Pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Set up the channel list
    global chan_list
    chan_list = [12, 16, 21]  # 12 red, 16 green, 21 blue
    GPIO.setup(chan_list, GPIO.OUT)
    
    # Initialize LED to green
    GPIO.output(chan_list, (False, True, False))
    
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
        GPIO.cleanup(chan_list)
        sys.exit(1)
