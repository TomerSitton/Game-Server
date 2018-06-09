

number_of_players = 0
"""The index of the player"""

class player:
    """
    This class represents a player with some fields
    """


    index = None
    """The index of the player"""

    address = ()
    """The address of the player, represented by (IP,PORT)"""
    player_socket = None
    """The socket of the player"""
    state = ""
    """The string describing the current state of the player, looking like this :[100,200]_F#2"""

    def __init__(self, player_socket, player_address):
        """
        This constructs a new Player with the given arguments
        :param player_socket: the socket of the player
        :param player_address: the address of the player
        """
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
        """
        This returns a string representing the player
        :return: a string representing the player
        """
        return "player number %d at address %r." % (self.index, self.address)
