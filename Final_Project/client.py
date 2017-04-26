#! /usr/bin/env python3

# Client script for connecting to servers

import socket
import sys

s = None


def main():
    global s

    host = '192.168.1.6'
    port = 50000
    size = 1024

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except socket.error as message:
        if s:
            s.close()
        print("Unable to open socket: " + str(message))
        sys.exit(1)

    while True:
        data = s.recv(size)
        print(data)


if __name__ == '__main__':
    try:
        main()
    except:
        print('Exiting program...')
        s.close()
        sys.exit(0)
