#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
import os
import json
from tornado import template
import socket
from time import sleep
import threading

import rasdrive_classes as RASD

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

#server_list = [RASD.RASD_Server('rasdserver1'), RASD.RASD_Server('rasdserver2')]
server_list = []
#backup_list = [RASD.RASD_Backup('rasdbackup1'), RASD.RASD_Backup('rasdbackup2')]
backup_list = []

# handle commands sent from the web browser
class CommandHandler(tornado.web.RequestHandler):
    # both GET and POST requests have the same responses
    def get(self, url='/'):
        print("get")
        self.handleRequest()

    def post(self, url='/'):
        global server_list
        global backup_list
        print('post')
        server_list = pickle.loads(self.request.body)['server_list']
        backup_list = pickle.loads(self.request.body)['backup_list']

    # handle both GET and POST requests with the same function
    def handleRequest(self):
        global server_list
        global backup_list
        
        # is op to decide what kind of command is being sent
        op = self.get_argument('op', None)

        # received a "checkup" operation command from the browser:
        if op == "status":
            print(backup_list)
            # make a dictionary
            status = {"server": True, "Servers Status": None, "Backups Status": backup_list[0].status.cpu_percent}
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


if __name__ == "__main__":
    application = make_app()
    port = 8888

    # start tornado
    application.listen(port)
    print("Starting server on port number {port}...".format(port=port))
    print("Open at http://{hostname}:{port}/index.html".format(hostname=os.uname()[1], port=port))
    tornado.ioloop.IOLoop.instance().start()

