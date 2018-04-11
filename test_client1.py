import socket

SERVER_ADDRESS = ("127.0.0.1",2212)


client_socket = socket.socket()

client_socket.connect(SERVER_ADDRESS)


client_socket.send("(53,53)\n")

while True:
    msg = client_socket.recv(1024)
    print msg
    if msg == "":
        break


client_socket.close()