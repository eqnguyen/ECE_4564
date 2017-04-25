#! /usr/bin/env python3

# This script contains code for the RasDrive tornado web server

import json
import os
import pickle
import socket

import rasdrive_classes as RASD
import tornado.ioloop
import tornado.web
from tornado import template

cwd = os.getcwd()  # used by static file server


# Return the IP address of host
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


# Send the index file
class IndexHandler(tornado.web.RequestHandler):
    def get(self, url='/'):
        self.render('index.html')

    def post(self, url='/'):
        self.render('index.html')


# Initialize RasDrive node lists
server_list = []
backup_list = []


# handle commands sent from the web browser
class CommandHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # Set header to handle cross-origin requests
        self.set_header("Access-Control-Allow-Origin", "http://rasdbackup1.local:8888")

    def get(self, url='/'):
        print("get")
        self.handleRequest()

    def post(self, url='/'):
        global server_list
        global backup_list

        print('post')

        server_list = pickle.loads(self.request.body)['server_list']
        backup_list = pickle.loads(self.request.body)['backup_list']

    # handle GET request
    def handleRequest(self):
        global server_list
        global backup_list

        # op to decide what kind of command is being sent
        op = self.get_argument('op', None)

        # received a "checkup" operation command from the browser:
        if op == "status":
            # make a dictionary
            status = {'servers': {}, 'backups': {}}

            # Update node status in dictionary
            for node in server_list + backup_list:
                if node_type(node) is RASD.RASD_SERVER:
                    node_type = 'servers'
                else:
                    node_type = 'backups'

                if node.status is None:
                    status[node_type][node.hostname] = {'online': False}
                else:
                    status['servers'][node.hostname] = {
                        'online': True,
                        'cpu': node.status.cpu_percent,
                        'net_stats': {
                            'bytes_sent': node.status.net_stats.bytes_sent,
                            'bytes_recv': node.status.net_stats.bytes_recv,
                            'errin': node.status.net_stats.errin,
                            'errout': node.status.net_stats.errout,
                            'dropin': node.status.net_stats.dropin,
                            'dropout': node.status.net_stats.dropout
                        },
                        'disk_usage': node.status.disk_usage
                    }

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
    print("Open at http://{ip}:{port}/index.html".format(ip=get_ip(), port=port))
    tornado.ioloop.IOLoop.instance().start()
