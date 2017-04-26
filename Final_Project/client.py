#! /usr/bin/env python3

# Client script for connecting to servers

import socket
import sys


def main():
    host = '192.168.1.6'
    port = 50000
    size = 1024
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.recv(size)
    except socket.error as message:
        if s:
            s.close()
        print("Unable to open socket: " + str(message))
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except:
        print('Exiting program...')
        sys.exit(0)
