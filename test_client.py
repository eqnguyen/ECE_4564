#!/usr/bin/env python3

import socket, pickle, hashlib, sys


# Receives all amounts of data from the server
def recvall(sock):
    buff_size = 1024  # 1 KiB

    sizeofmsg = int(sock.recv(buff_size))
    print("SIZE: " + str(sizeofmsg))

    msg = sock.recv(sizeofmsg)
    counter = 1
    while len(msg) < sizeofmsg:
        print(counter)
        msg += recvall(sock)
        counter += 1

    # while True:
    # part = sock.recv(buff_size)
    # data += part
    # if len(part) < buff_size:
    # either 0 or end of data
    # break
    return msg


host = input("Enter server IP address: ")
port = 50000
size = 1024

# Queries user for input
query = input("Enter your question: ")

while query != "quit":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except socket.error as message:
        if s:
            s.close()
        print("Unable to open socket: " + str(message))
        sys.exit(1)

    tup = (query, hashlib.md5(query.encode()).digest())
    s.send(pickle.dumps(tup))

    while 1:
        data = recvall(s)

        try:
            tup = pickle.loads(data)
            print("Answer: " + tup[0])
            break
        except Exception as inst:
            print(inst)
            print("Pickle failure")
            errormsg = "ERROR CODE: 2"
            errortup = (errormsg, hashlib.md5(errormsg.encode()).digest())
            s.send(pickle.dumps(errortup))

    query = input("Enter your question: ")
    s.close()
