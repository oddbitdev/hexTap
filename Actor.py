__author__ = 'oddBit'

from kivy.uix.image import Image
from data.gameData import *
from random import choice


class Actor(Image):
    def __init__(self, col, row, actor_type=None, ended_turn=False, **kwargs):
        super(Actor, self).__init__(**kwargs)
        self.col = col
        self.row = row
        self.ended_turn = ended_turn
        if actor_type:
            self.actor_type = actor_type
        else:
            self.actor_type = choice(enemies)
        if self.actor_type in flyables:
            self.can_fly = True
        else:
            self.can_fly = False
        self.source = 'assets/graphics/enemies/' + self.actor_type + choice(['Left', 'Right']) + '.zip'

    def move_left(self):
        self.source = 'assets/graphics/enemies/' + self.actor_type + 'Left' + '.zip'

    def move_right(self):
        self.source = 'assets/graphics/enemies/' + self.actor_type + 'Right' + '.zip'