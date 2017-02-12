#!/usr/bin/python

import socket, pickle, hashlib

host = '192.168.0.104'
port = 50000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Queries user for input
query = input("Enter your question: ")

s.connect((host,port))

tup = (query, hashlib.md5(query.encode()).digest());
s.send(pickle.dumps(tup))

data = s.recv(size)

tup = pickle.loads(data)
print("Answer: " + tup[0])
