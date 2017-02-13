#!/usr/bin/python

import socket, pickle, hashlib


# Receives all amounts of data from the server
def recvall(sock):
    buff_size = 1024  # 4 KiB

    sizeofmsg = sock.recv(buff_size)
    print("SIZE: " + str(sizeofmsg))
    msg = sock.recv(int(sizeofmsg))

    # while True:
    # part = sock.recv(buff_size)
    # data += part
    # if len(part) < buff_size:
    # either 0 or end of data
    # break
    return msg


host = '192.168.0.101'
port = 50000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Queries user for input
query = input("Enter your question: ")

s.connect((host, port))

tup = (query, hashlib.md5(query.encode()).digest());
s.send(pickle.dumps(tup))

data = recvall(s)

try:
    tup = pickle.loads(data)
    print("Answer: " + tup[0])
except:
    print("Pickle failure")
    errormsg = "ERROR CODE: 2"
    errortup = (errormsg, hashlib.md5(errormsg.encode()).digest())
    s.send(errortup)
