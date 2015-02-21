__author__ = 'YuChen'

class Card:
    """ a class that represents a card populated with a github project """
    def __init__(self, usr, name, img, description):
        self.username = usr
        self.name = name
        self.image = img
        self.description = description
