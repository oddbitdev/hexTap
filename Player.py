__author__ = 'oddBit'

from kivy.uix.image import Image
from random import choice
from data.gameData import *


class Player(Image):
    def __init__(self, stars, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.state = PlayerStates.SIT_LEFT
        self.source = player_sprites[self.state]
        self.stars = stars
        self.anim_delay = 0.2

    def select_player(self):
        if self.state == PlayerStates.SIT_LEFT:
            self.state = PlayerStates.SIT_LEFT_SELECTED
        else:
            self.state = PlayerStates.SIT_RIGHT_SELECTED
        self.source = player_sprites[self.state]

    def stop_player(self):
        self.state = choice([PlayerStates.SIT_LEFT, PlayerStates.SIT_RIGHT])
        self.source = player_sprites[self.state]

    def move_left(self):
        self.state = PlayerStates.WALK_LEFT
        self.source = player_sprites[self.state]

    def move_right(self):
        self.state = PlayerStates.WALK_RIGHT
        self.source = player_sprites[self.state]

    def jump_left(self):
        self.state = PlayerStates.JUMP_LEFT
        self.source = player_sprites[self.state]

    def jump_right(self):
        self.state = PlayerStates.JUMP_RIGHT
        self.source = player_sprites[self.state]

    def player_dead(self):
        self.state = PlayerStates.DEAD
        self.source = player_sprites[self.state]

    def add_star(self):
        self.stars += 1

    def use_star(self):
        self.stars -= 1