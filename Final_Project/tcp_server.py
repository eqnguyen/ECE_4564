#! /usr/bin/env python3

# Socket server which accepts connections from clients and sends
# the list of clients to the tornado web server

import pickle
import requests
import socket
import select
import sys


# Return the IP address of host
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def post_clients(client_list):
    s = requests.Session()
    payload = pickle.dumps({'client_list': client_list})
    try:
        s.post("http://localhost:8888/com/clients", data=payload)
    except:
        print('Could not post status to server')


def main():
    connection_list = []  # List of socket clients
    client_list = []  # List of client ip addresses
    port = 50000
    server_socket = ''
    server_address = get_ip()

    # Reset client list on server
    post_clients(client_list)

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_address, port))
        server_socket.settimeout(5)
        server_socket.listen(5)
    except socket.error as message:
        if server_socket:
            server_socket.close()
        print('Could not open socket:', message)
        sys.exit(1)

    # Add server socket to the list of readable connections
    connection_list.append([server_socket, server_address])

    print("Starting tcp server on {ip}:{port}".format(ip=server_address, port=port))

    while True:
        # Get the list sockets which are ready to be read through select

        for (sock, sock_address) in connection_list:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection received through server_socket
                try:
                    client, address = server_socket.accept()
                    connection_list.append([client, address])
                    client_list.append(address[0])
                    print("Client connected: ", address[0])
                    post_clients(client_list)
                except:
                    pass
            else:
                try:
                    sock.send(b'ping')
                # Client disconnected, so remove from socket list
                except:
                    print("Client disconnected: ", sock_address[0])
                    sock.close()
                    connection_list.remove([sock, sock_address])
                    client_list.remove(sock_address[0])
                    post_clients(client_list)
                    continue


if __name__ == "__main__":
    try:
        main()
    except:
        print('Exiting program...')
        sys.exit(0)
