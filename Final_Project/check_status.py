#! /usr/bin/env python3

from aiocoap import *
import asyncio
from time import sleep
import rasdrive_classes as RASD
import requests
import sys
import pickle


async def checkStatus():
    server_list = [RASD.RASD_Server('rasdserver1'), RASD.RASD_Server('rasdserver2')]
    backup_list = [RASD.RASD_Backup('rasdbackup1'), RASD.RASD_Backup('rasdbackup2')]

    protocol = await Context.create_client_context()
    s = requests.Session()

    while True:
        for server in server_list:
            # Get statuses from servers
            request = Message(code=GET, uri='coap://{hostname}.local/status'.format(hostname=server.hostname))

            try:
                response = await protocol.request(request).response
            except:
                # presumably server went offline...deal with it here
                print('Failed to fetch resource from:', server.hostname)
                server.status = None
            else:
                tup = pickle.loads(response.payload)
                print(tup)
                server.status = tup

        for backup in backup_list:
            # Get statuses from backups
            request = Message(code=GET, uri='coap://{hostname}.local/status'.format(hostname=backup.hostname))

            try:
                response = await protocol.request(request).response
            except Exception:
                # presumably server went offline...deal with it here
                print('Failed to fetch resource from:', backup.hostname)
                backup.status = None
            else:
                tup = pickle.loads(response.payload)
                print(tup)
                backup.status = tup

        payload = pickle.dumps({"server_list": server_list, "backup_list": backup_list})
        s.post("http://localhost:8888/com", data=payload)
        sleep(10)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(checkStatus())
        loop.close()
    except:
        print('Exiting program...')
        sys.exit(1)
