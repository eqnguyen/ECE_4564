#! /usr/bin/env python3

# Client script for connecting to RasDrive servers

import argparse
import pickle
import socket
import sys
from subprocess import call


# Return the IP address of host
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def sync(ip_list):
    for ip in ip_list:
        command = './test_rsync_win/bin/rsync.exe -av -e ./test_rsync_win/bin/ssh pi@' + ip + ':~/rsyncTests/ ./test_rsync_win/BackupDir/'
        call(command.split(" "))

        command = './test_rsync_win/bin/rsync.exe -av -e ./test_rsync_win/bin/ssh ./test_rsync_win/BackupDir/ pi@' + ip + ':~/rsyncTests/'
        call(command.split(" "))


s = None
server_socket = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address")
    args = parser.parse_args()

    global s
    global server_socket
    host = args.ip_address
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
        try:
            s.recv(size)
            client, address = server_socket.accept()
            client.settimeout(5)
            tup = pickle.loads(client.recv(size))

            if tup[0] == 'Now':
                print('Syncing now to:', tup[1])
                sync(tup[1])
            else:
                print('Sync scheduled for:', tup[0])

            client.close()
        except ConnectionResetError:
            print('Server is offline')
            raise
        except socket.timeout:
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
