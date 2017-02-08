#!/usr/bin/python

import socket


host = '172.29.56.50'
port = 50000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Queries user for input
query = input("Enter your question: ")

s.connect((host,port))
s.send(query.encode())

data = s.recv(size)

print(data.decode())
