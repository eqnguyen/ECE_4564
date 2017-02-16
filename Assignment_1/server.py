#! /usr/bin/env python3

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import socket, json, sys, os
import wolfram_alpha
import pickle
import hashlib

# --------------- GETS W|A api appID ------------------------
try:
    f = open("api_keys.txt", "r")
except FileNotFoundError as inst:
    print("The file 'api_keys.txt' was not found")
    exit()

line = f.readline()
while "Wolfram|Alpha appID : " not in line and line != "":
    line = f.readline()

try:
    appID = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Wolfram|Alpha appID in 'api_keys.txt'")
    exit()

# -----------------------------------------------------------


def sendwithsize(sock, msgtup):
    msg = pickle.dumps(msgtup)
    sock.send(str(len(msg)).encode())
    sock.send(msg)


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

# Print host IP address
print("Host: " + os.popen("hostname -I").read())
print("Port: " + str(port))
print("Now listening . . .")

emptymsg = '["idiot"]'
answertup = (emptymsg, hashlib.md5(emptymsg.encode()).digest())

# create a new instance of the wolfram class
w = wolfram_alpha.wolfram(appID)

while 1:
    try:
        client, address = s.accept()
        badresponse = True
        while badresponse:
            data = client.recv(size)

            if not data:
                client.close()
                print("Empty message, aka client closed socket")
                client, address = s.accept()
                continue

            print("Data: ", data)
            tup = pickle.loads(data)
            print(tup)

            if tup[0] == "ERROR CODE: 2":
                # got a resend request
                print("Resending message")
                sendwithsize(client, answertup)
                badresponse = True
            elif tup[1] == hashlib.md5(tup[0].encode()).digest():
                # checksum checks out
                print("Checksum checks out")
                query = tup[0]
                badresponse = False
            else:
                # make request for resend
                errormsg = "ERROR CODE: 2"
                errortup = (errormsg, hashlib.md5(errormsg.encode()).digest())

                print("Error: checksum failed, requesting resend")

                # send resend request
                # client.send(pickle.dumps(errortup))
                sendwithsize(client, errortup)
                badresponse = True

        print("Starting search...")
        answer = w.search(query)
        print("Search finished")

        if answer:
            answertext = json.dumps(answer)
            answertup = (answertext, hashlib.md5(answertext.encode()).digest())
            print(answertext)
        else:
            # if no answers were received
            # noanswermsg is json formatted as a list containing one string, "W|A returned no answers"
            noanswermsg = '["W|A returned no answers"]'
            print(noanswermsg)
            answertup = (noanswermsg, hashlib.md5(noanswermsg.encode()).digest())

        sendwithsize(client, answertup)
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

        # this allows us to see the line number and filename where the exception ocurred
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        errormsg = "ERROR CODE: 1"
        errortup = (errormsg, hashlib.md5(errormsg.encode()).digest())

        # client.send(pickle.dumps(errortup))
        sendwithsize(client, errortup)
