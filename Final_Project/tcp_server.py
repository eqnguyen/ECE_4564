#! /usr/bin/env python3

# Socket server which accepts connections from clients and sends
# the list of clients to the tornado web server

import pickle
import requests
import socket
import select
import sys


def main():
    connection_list = []  # list of socket clients
    client_list = []
    size = 1024
    port = 50000
    server_address = socket.gethostbyname(socket.gethostname())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)

    # Add server socket to the list of readable connections
    connection_list.append(server_socket)

    print("Server started on {ip}:{port}".format(ip=server_address, port=port))

    s = requests.Session()

    while True:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(connection_list, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection received through server_socket
                sockfd, addr = server_socket.accept()
                connection_list.append(sockfd)
                client_list.append(addr)
                print("Client connected: ", addr)
                payload = pickle.dumps({'client_list': client_list})
                try:
                    s.post("http://localhost:8888/com/clients", data=payload)
                except:
                    print('Could not post status to server')

            # Some incoming message from a client
            else:
                # Data received from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(size)
                    # echo back the client message
                    if data:
                        print(data)

                # Client disconnected, so remove from socket list
                except:
                    print("Client disconnected: ", addr)
                    sock.close()
                    connection_list.remove(sock)
                    client_list.remove(addr)

                    payload = pickle.dumps({'client_list': client_list})
                    try:
                        s.post("http://localhost:8888/com/clients", data=payload)
                    except:
                        print('Could not post status to server')

                    continue


if __name__ == "__main__":
    try:
        main()
    except:
        print('Exiting program...')
        sys.exit(0)
