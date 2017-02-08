#!/usr/bin/python

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import socket, json, sys, os
import wolfram_alpha

# Thomas's appid
appID = '43UVWL-U3JYWWV895'

host = ''
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

s.listen(backlog)

while 1:
    try:
        client, address = s.accept()
        data = client.recv(size)
        print(b'Data recieved: ' + data)
        data = data.decode()  # json.loads(data.decode())

        # Queries user for input
        query = data

        # create a new instance of the wolfram class
        w = wolfram_alpha.wolfram(appID)

        answer = w.search(query)

        # just prints the json returned
        print(answer)

        client.send(answer.encode())
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        client.send(b'ERROR')
