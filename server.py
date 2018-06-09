import socket
from threading import Thread, _sleep
import Player

android_socket = None
"""The android socket"""
server_socket = None
"""The server socket"""
# The server address data
IP = "0.0.0.0"
"""The server's IP address"""
PORT = 2212
"""The port on which the program runs on"""
SERVER_ADDRESS = (IP, PORT)
"""The full address of the program"""

players = []
"""The list of connected players"""

winners_index = -1
"""The index of the winner"""

def init_server():
    """ This method creates the server socket and binds it to the correct address """

    global server_socket
    # creating a server socket
    server_socket = socket.socket()

    # binding the server socket to the wanted adress
    server_socket.bind(SERVER_ADDRESS)



def handle_clients_connection():
    """ This method handles the connection of the clients to the server """
    global server_socket
    global players
    # setting client's queue length
    server_socket.listen(5)
    print "server online. waiting for players"

    while len(players) < 2:
        _accept_client(server_socket)

    print "there are 2 players. waiting for more...?"

    while len(players) < 4:
        send_msg_to_players(players, "we are %d players. more players?" % len(players))
        print "we are %d players. more players?" % len(players)
        if "yes" in receive_msg_from_players():
            _accept_client(server_socket)
        else:
            send_msg_to_players(players, "the final number of players is %d" % len(players))
            print "the final number of players is %d" % len(players)
            break

    send_msg_to_players(players,"start game")
    print "start game"


def _accept_client(server_socket):
    """
    This method is responsible of connecting a player to the
    server and adding him to the list of connected players
    :param server_socket: the socket of the server
    :return: None
    """
    (player_socket, player_address) = server_socket.accept()
    print "a player has joind the game!"
    new_player = Player.player(player_socket=player_socket, player_address=player_address)
    players.append(new_player)
    # send the index of the player to that player
    new_player.player_socket.send(str(new_player.index) + "\n")


def update_player_location(player):
    """
    This method receives data from a player and updates its "state" field
    :param player: the player of which the method needs to update the location
    :return: None
    """
    global winners_index
    print "started handling requests for player: %r" % str(player)
    msg = str(player.player_socket.recv(32768))
    while msg != "finished!":
        if msg != "":
            player.state = msg.strip("\n") + " ~ "
        msg = str(player.player_socket.recv(32768))

    msg = str(player.player_socket.recv(32768))
    if msg != "" and int(msg.split()[1]) == player.index:
        winners_index = player.index


def send_msg_to_players(players, msg=""):
    """
    sends the data msg received as a parameter to all the players
    :param players: the list of players
    :param msg: the msg to send to players
    :return: None
    """
    for player in players:
        player.player_socket.send(msg + "\n")


def receive_msg_from_players():
    """
    creates a long msg from the data received from all the player
    :return: a string representing the data sent from all of the players
    """
    msg = []
    for i, player in enumerate(players):
        single_msg =  player.player_socket.recv(32768)
        print "received %s" % single_msg
        msg.append(single_msg)
    return msg

def android():
    """
    handle android connection
    :return: None
    """
    global android_socket
    (android_socket, android_address) = server_socket.accept()


if __name__ == "__main__":

    # initialize the server socket
    init_server()

    # wait for players to connect and connect them to the game server
    handle_clients_connection()

    # handle android stuff
    Thread(name="android", target=android).start()

    # start a request-handling thread for each player
    for player in players:
        player_requests_thread = Thread(name="player %d requests thread" % player.index, target=update_player_location,
                                        args=[player])
        player_requests_thread.start()

    msg = ""
    # send data about the players in this format:
    # "[newX1,newY1]_attack#health ~ [newX2,newY2]_attack#health ~ [newX3,newY3]_attack#health ~ [newX4,newY4]_attack#health ~\n"
    while winners_index == -1:
        healths = ""
        for client in players:
            for p in players:
                if msg == "":
                    msg = p.state
                else:
                    msg = msg + p.state

            if client.state != "":
                healths = healths + "player " + str(client.index) + " : " + client.state[-4]+ " \t"

            if msg is not "" and msg.count('[') == len(players):
                client.player_socket.send(msg + "\n")
                print "sent %r" % (msg + "\n")
            msg = ""

        print healths + "\n"
        if android_socket != None:
            android_socket.send(healths + "\n")
        _sleep(0.05)

    for client in players:
        client.player_socket.send(str(winners_index) + "\n")
    android_socket.send(str(winners_index) + "\n")
    print "sent %r" % (str(winners_index) + "\n")
    server_socket.close()
