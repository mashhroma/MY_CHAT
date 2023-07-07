#!/bin/python3
import socket
import threading

# Connection Data
host = '185.211.170.104'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
users = {}

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in users:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
            print(message)
        except:
            # Removing And Closing Clients
            broadcast('{} left!'.format(users.get(client)).encode(encoding='utf-8'))
            users.pop(client)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode(encoding='utf-8'))
        nickname = client.recv(1024).decode(encoding='utf-8')
        users[client] = nickname

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode(encoding='utf-8'))
        client.send('Connected to server!'.encode(encoding='utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")

receive()
