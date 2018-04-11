import socket
server_socket = None

def init_server():
    global server_socket
    # creating a server socket
    server_socket = socket.socket()

    # binding the server socket to the wanted adress
    server_socket.bind(('0.0.0.0',3339))

if __name__ == '__main__':
    init_server()
    server_socket.listen(1)

    (client_socket, client_address) = server_socket.accept()

    request = client_socket.recv(1024)
    print "bla"
    print request