
# the index of the player
number_of_players = 0

class player:
    # the index of the player
    index = None
    # the address of the player, repressented by (IP,PORT)
    address = ()
    # the socket of the player
    player_socket = None
    # the player's location on the board. repressented by ['x','y']
    location = [0 , 0]

    def __init__(self, player_socket, player_address):
        global number_of_players

        # set the index of the player
        self.index = number_of_players + 1

        # set the address of the player
        self.address = player_address

        # set the socket of the player
        self.player_socket = player_socket

        # increase the number of players
        number_of_players += 1

    def __str__(self):
        return "player number %d at address %r. Located at %r" % (self.index, self.address, self.location)