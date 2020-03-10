# coding: utf8

from utils import rotation, init_sommets
print(">> Loading module: 'objects'...")


class Mobile:

    def __init__(self, dimensions):
        """
        initializes a mobile
        USING: - Coord6d
               - init_sommets
        """
        pass

    def move(self, spatial, angular):
        """
        moves the mobile
        USING: - change_spatial
               - change_angular
        """
        pass


class Hangar:

    def __init__(self, dimensions):
        """
        initializes the hangar
        USING: - Coord6d
        """
        pass


class Coord6d:

    def __init__(self, x=0, y=0, z=0, alpha=0, beta=0, gamma=0):
        """
        initializes the 6 coordinates
        """

    def change_spatial(self, spatial):
        """
        change the angular coordinates
        cf reconstruction_coins
        """
        pass

    def change_angular(self, angular):
        """
        change the angular coordinates
        USING: - rotation
        cf reconstruction_coins
        """
        pass
