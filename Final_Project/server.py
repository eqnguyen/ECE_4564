#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
import os
import json
from tornado import template
import socket

import asyncio
import pickle
from aiocoap import *

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

cwd = os.getcwd()  # used by static file server


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        t = template.Template("<html>{{ myvalue }}</html>")
        self.write(t.generate(myvalue="XXX"))


# send the index file
class IndexHandler(tornado.web.RequestHandler):
    def get(self, url='/'):
        self.render('index.html')

    def post(self, url='/'):
        self.render('index.html')


# handle commands sent from the web browser
class CommandHandler(tornado.web.RequestHandler):
    # both GET and POST requests have the same responses
    def get(self, url='/'):
        print("get")
        self.handleRequest()

    def post(self, url='/'):
        print('post')
        self.handleRequest()

    # handle both GET and POST requests with the same function
    def handleRequest(self):
        # is op to decide what kind of command is being sent
        op = self.get_argument('op', None)

        # received a "checkup" operation command from the browser:
        if op == "status":
            # make a dictionary
            status = {"server": True, "mostRecentSerial": "test"}
            # turn it to JSON and send it to the browser
            self.write(json.dumps(status))

        # operation was not one of the ones that we know how to handle
        else:
            print("op: {op}".format(op=op))
            print(self.request)


def make_app():
    return tornado.web.Application([
        # all commands are sent to http://*:port/com
        # each command is differentiated by the "op" (operation) JSON parameter
        (r"/(com.*)", CommandHandler),
        (r"/", IndexHandler),
        (r"/(index\.html)", tornado.web.StaticFileHandler, {"path": cwd}),
])

servers_list = []

async def checkStatus():
    protocol = await Context.create_client_context()

    for server in servers_list:
        # Get statuses from servers
        request = Message(code=GET, uri='coap://{ip}/status'.format(ip=server.ip))

        try:
            response = await protocol.request(request).response
        except Exception as e:
            # presumably server went offline...deal with it here
            print('Failed to fetch resource:')
            print(e)
        else:
            tup = pickle.loads(response.payload)
            print('Result: {code}\n{data}'.format(code=response.code, data=tup))

if __name__ == "__main__":
    application = make_app()
    port = 8888
    # tell tornado to run checkSerial every 5000ms
    status_loop = tornado.ioloop.PeriodicCallback(checkStatus, 5000)
    status_loop.start()

    # start tornado
    application.listen(port)
    print("Starting server on port number {port}...".format(port=port))
    print("Open at http://{ip}:{port}/index.html".format(ip=getIP(), port=port))
    tornado.ioloop.IOLoop.instance().start()