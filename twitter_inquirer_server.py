#!/usr/bin/python

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import socket, json
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
    client, address = s.accept()
    data = client.recv(size)
    data = json.loads(data)

    # Queries user for input
    query = data

    # create a new instance of the wolfram class
    w = wolfram_alpha.wolfram(appID)

    answer = w.search(query)

    # just prints the json returned
    print(answer)

    client.send(answer)
