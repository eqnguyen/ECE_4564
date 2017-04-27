#! /usr/bin/env python3

# Client script for connecting to servers

import socket
import sys


# Return the IP address of host
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


s = None
server_socket = None

def main():
    global s
    global server_socket
    host = '192.168.1.6'
    conn_port = 50000
    server_port = 25000
    size = 1024

    server_address = get_ip()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, conn_port))
        s.settimeout(5)
    except socket.error as message:
        if s:
            s.close()
        print("Unable to open socket: " + str(message))
        sys.exit(1)

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_address, server_port))
        server_socket.settimeout(5)
        server_socket.listen(5)
    except socket.error as message:
        if server_socket:
            server_socket.close()
        print('Could not open socket:', message)
        sys.exit(1)

    while True:
        s.recv(size)
        try:
            client, address = server_socket.accept()
            client.settimeout(5)
            data = client.recv(size)
            if data:
                print(data)
            client.close()
        except:
            pass


if __name__ == '__main__':
    try:
        main()
    except:
        print('Exiting program...')
        if s:
            s.close()
        if server_socket:
            server_socket.close()
        sys.exit(0)
