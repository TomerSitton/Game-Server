import socket

SERVER_ADDRESS = ("127.0.0.1",2212)


client_socket = socket.socket()

client_socket.connect(SERVER_ADDRESS)


client_socket.send("player 3 connected")
