#!/usr/bin/python

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import socket, json, sys, os
import wolfram_alpha
import pickle
import hashlib

# Thomas's appid
appID = '43UVWL-U3JYWWV895'

host = ''
port = 50000
backlog = 5
size = 1024

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(backlog)
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)

while 1:
    try:
        client, address = s.accept()
        data = client.recv(size)
        print(b'Data recieved: ' + data)
        tup = pickle.loads(data)
        print(tup[0])
        query = tup[0]

        # create a new instance of the wolfram class
        w = wolfram_alpha.wolfram(appID)

        answer = w.search(query)
        tup = (answer[0], hashlib.md5(answer[0].encode()).digest());

        if answer:
            # just prints the json returned
            print(answer[0])
            client.send(pickle.dumps(tup))
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        client.send(b'ERROR')