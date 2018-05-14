import socket
from threading import Thread, _sleep
import Player

# The server address data
IP = "0.0.0.0"
PORT = 2212
SERVER_ADDRESS = (IP, PORT)

# The time to wait to playes to connect to the server
CONNECTION_TIMEOUT = 15

# The list of connected players
players = []

"""
This method creates the server socket and binds it to the correct address
"""


def init_server():
    global server_socket
    # creating a server socket
    server_socket = socket.socket()

    # binding the server socket to the wanted adress
    server_socket.bind(SERVER_ADDRESS)


"""
This method handles the connection of the clients to the server
"""


def handle_clients_connection(connection_timeout):
    global server_socket
    global players
    # setting client's queue length
    server_socket.listen(4)
    print "waiting for players"

    # run the accept_clients thread for the connection timeout
    t = Thread(target=_accept_clients, args=[server_socket])
    t.start()
    t.join(timeout=connection_timeout)

    print "time to connect is up! or there are already 4 players! we are full!"

    # send the number of players to all the players
    for player in players:
        player.player_socket.send(str(len(players)) + "\n")


"""This method is responsible of connecting the players to the server and adding them to the list of connected players"""


def _accept_clients(server_socket):
    while len(players) < 4:
        (player_socket, player_address) = server_socket.accept()
        print "a player has joind the game!"
        new_player = Player.player(player_socket=player_socket, player_address=player_address)
        players.append(new_player)
        # send the index of the player to that player
        new_player.player_socket.send(str(new_player.index) + "\n")


def update_player_location(player):
    print "started handling requests for player: %r" % str(player)
    while True:
        msg = str(player.player_socket.recv(32768))
        if msg != "":
            player.state = msg.strip("\n") + " ~ "

if __name__ == "__main__":

    # initialize the server socket
    init_server()

    # wait for players to connect and connect them to the game server
    handle_clients_connection(connection_timeout=CONNECTION_TIMEOUT)

    # start a request-handling thread for each player
    for player in players:
        player_requests_thread = Thread(name="player %d requests thread" % player.index, target=update_player_location,
                                        args=[player])
        player_requests_thread.start()
    # send data about the players in this format:
    # "health_[newX1,newY1]_attack ~ health_[newX2,newY2]_attack ~ health_[newX3,newY3]_attack ~ health_[newX4,newY4]_attack ~ \n"
    msg = ""
    while True:
        for client in players:
            for p in players:
                if msg == "":
                    msg = p.state
                else:
                    msg = msg + p.state

            if msg is not "":
                client.player_socket.send(msg + "\n")
                print "sent %r"%(msg + "\n")
            msg = ""
        _sleep(0.05)
