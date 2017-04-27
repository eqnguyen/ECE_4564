#! /usr/bin/env python3

# Client script for connecting to RasDrive servers

import argparse
import datetime
import pickle
import socket
import sys

from subprocess import call
from threading import Timer


# Return the IP address of host
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def sync(ip_list):
    platform = sys.platform
    sync_command = ''
    backup_command = ''

    for ip in ip_list:
        if platform == 'win32':
            sync_command = './rsync/bin/rsync.exe -av -e ./rsync/bin/ssh pi@{ip}'.format(
                ip=ip) + ':~/rsyncTests/ ./BackupDir/'
            backup_command = './rsync/bin/rsync.exe -av -e ./rsync/bin/ssh ' \
                             './BackupDir/ pi@{ip}'.format(ip=ip) + ':~/rsyncTests/'
        elif platform == 'linux':
            sync_command = 'rsync -av -e ssh pi@{ip]'.format(ip=ip) + ':~/rsyncTests/ ./BackupDir/'
            backup_command = 'rsync -av -e ssh ./BackupDir/ pi@{ip}'.format(ip=ip) + ':~/rsyncTests/'

        call(sync_command.split(" "))
        call(backup_command.split(" "))


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
            (t, ip_list) = pickle.loads(client.recv(size))

            if t == 'Now':
                print('\nSyncing now to:', ip_list)
                sync(ip_list)
            else:
                scheduled_date, scheduled_time = t.split('T')
                year, month, day = map(int, scheduled_date.split('-'))
                hour, minute = map(int, scheduled_time.split(':'))
                date = datetime.datetime(year, month, day, hour, minute)
                delay = (date - datetime.datetime.now()).total_seconds()
                print('\nSync scheduled for:', date, 'in', delay, 'seconds')
                Timer(delay, sync, kwargs={'ip_list': ip_list}).start()

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
