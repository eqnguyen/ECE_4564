#!/usr/bin/python

import socket, pickle

host = '192.168.0.104'
port = 50000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Queries user for input
query = input("Enter your question: ")

s.connect((host,port))
s.send(pickle.dumps(query.encode()))

data = s.recv(size)

tup = pickle.loads(data)
print("Answer: " + tup[0])
