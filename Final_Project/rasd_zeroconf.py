#! /usr/bin/env python3

import socket
import pickle
import rasdrive_classes as RASD

max_nodes = 5
port = 22222

priority = 1
server_list = []
backup_list = []


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def start_up():
    s = socket.socket()
    s.settimeout(5)  # 5 seconds

    first_rasdrive = False

    try:
        s.connect(('raspberrypi.local', port))  # "random" IP address and port
    except socket.error as exc:
        # couldn't connect, therefore this guy must be the first to be brought online
        first_rasdrive = True
        print("Caught exception socket.error : {exception}".format(exception=exc))

    if first_rasdrive:
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.bind((socket.gethostname(), port))
        # become a server socket
        serversocket.listen(max_nodes)

        while True:
            # accept connections from outside
            (clientsocket, address) = serversocket.accept()
            type = clientsocket.recv(30)

            if type == "server":
                server_list.append(RASD.RASD_Server(ip=address, priority=priority, status=None))
                priority = priority + 1
                clientsocket.send(pickle.dumps({"servers": server_list, "backup pis": backup_list}))
            elif type == "backup":
                backup_list.append(RASD.RASD_Backup(ip=address, status=None))
