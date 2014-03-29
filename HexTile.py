__author__ = 'oddBit'

from kivy.uix.image import Image
from kivy.animation import Animation
from Player import Player
from data.gameData import *
from random import choice, random


def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


class HexTile(Image):
    def __init__(self, row, col, type, level, has_actor, has_star, has_player, key_type, exit_type, **kwargs):
        super(HexTile, self).__init__(**kwargs)
        self.row = row
        self.col = col
        self.type = type
        self.level = level
        self.bubble = False
        self.actor = None
        self.player = None
        self.mod_layer = None
        self.game_map = None
        self.has_player = has_player
        self.star = None
        self.key = None
        self.exit = None
        self.key_type = key_type
        self.exit_type = exit_type
        self.occupied = False
        self.portal = None
        if random() < 0.7:
            self.add_mod_layer()
        if has_star:
            self.add_star()
        if key_type:
            self.add_key()
        if exit_type:
            self.add_exit()
        if self.portal:
            self.add_portal()
        if has_actor:
            self.add_actor()

    def post_init(self):
        self.game_map = self.parent.parent

    def on_touch_up(self, touch):
        if abs(touch.time_end - touch.time_start) < 0.18:
            x, y = self.to_local(touch.x, touch.y)
            if in_circle(self.x + self.width / 2, self.y + 244 + self.width / 2, self.width / 2, x, y) \
                    and ((not self.bubble and not self.game_map.has_bubble and not self.game_map.is_moving) or
                             (self.game_map.is_move_mode and self.player and not self.game_map.is_moving)):
                if not self.player:
                    if not self.game_map.is_move_mode and not self.game_map.is_just_selected:
                        self.game_map.add_bubble(self.pos, self.id, self)
                        self.bubble = True
                    elif not self.game_map.is_just_selected:
                        self.game_map.schedule_move_to_hex(self)
                elif self.player and not self.game_map.is_move_mode:
                    self.game_map.move_mode(self)
                elif self.player and self.game_map.is_move_mode:
                    self.game_map.is_move_mode = False
                    self.player.stop_player()
                    self.game_map.add_bubble(self.pos, self.id, self)
                    self.game_map.remove_skip_turn()
                    self.bubble = True
            else:
                self.game_map.remove_bubble(self.id)
                self.bubble = False
        else:
            if self.bubble:
                self.game_map.remove_bubble(self.id)
                self.bubble = False

    def add_portal(self):
        self.portal = Image(source='assets/graphics/tiles/portal.png', pos=(self.x + 10, self.y + 264))
        self.add_widget(self.portal)

    def remove_portal(self):
        self.remove_widget(self.portal)
        self.portal = None

    def move_portal(self):
        if self.level == MAX_LEVEL:
            self.move_down(False)
        elif self.level == 0:
            self.move_up(False)
        else:
            self.move_up(False) if random() > 0.5 else self.move_down(False)

    def add_actor(self, actor_to_transfer=None):
        self.occupied = True
        self.actor = True

    def remove_actor(self, a=0, b=0):
        self.actor = False
        self.occupied = False

    def add_key(self):
        self.key = Image(source='assets/graphics/tiles/' + self.key_type + '.png', pos=(self.x + 20, self.y + 274))
        self.add_widget(self.key)

    def remove_key(self, a, b):
        if self.key:
            self.remove_widget(self.key)
            self.key = None
            self.key_type = None

    def add_exit(self):
        self.exit = Image(source='assets/graphics/tiles/' + self.exit_type + '.png', pos=(self.x + 10, self.y + 264))
        self.add_widget(self.exit)

    def remove_exit(self, a, b):
        if self.exit:
            self.remove_widget(self.exit)
            self.exit = None
            self.exit_type = None

    def add_star(self):
        self.star = Image(source='assets/graphics/tiles/starGold.png', pos=(self.x + STAR_POS[0],
                                                                            self.y + STAR_POS[1] + 204))
        self.add_widget(self.star)

    def remove_star(self, a, b):
        if self.star:
            self.remove_widget(self.star)
            self.star = None

    def add_mod_layer(self):
        mod_type = choice(mod_layers)
        self.mod_layer = Image(source='assets/graphics/tiles/' + mod_type + '.png',
                               pos=(self.x, self.y + 204), size=(120, 210))
        self.add_widget(self.mod_layer)

    def add_player(self, stars=23, position=None):
        if position:
            self.player = Player(stars, pos=(position[0], position[1]))
        else:
            self.player = Player(stars, pos=(self.pos[0] + 10, self.pos[1] + 279))
        self.add_widget(self.player)

    def remove_player(self):
        if self.player:
            self.remove_widget(self.player)
            self.player = None

    def move_up(self, use_star):
        if self.level == MAX_LEVEL:
            return
        self.level += 1
        anim = Animation(y=self.pos[1] + 34, t='in_out_elastic', duration=.7)
        anim.start(self)
        if self.player:
            actor_anim = Animation(y=self.player.pos[1] + 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.player)
        if self.mod_layer:
            actor_anim = Animation(y=self.mod_layer.pos[1] + 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.mod_layer)
        if self.star:
            actor_anim = Animation(y=self.star.pos[1] + 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.star)
        if self.key:
            actor_anim = Animation(y=self.key.pos[1] + 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.key)
        if self.exit:
            actor_anim = Animation(y=self.exit.pos[1] + 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.exit)
        if self.portal:
            portal_anim = Animation(y=self.portal.pos[1] + 34, t='in_out_elastic', duration=.7)
            portal_anim.start(self.portal)
        if use_star:
            self.game_map.tile_with_player.player.use_star()

    def move_down(self, use_star):
        if self.level == 0:
            return
        self.level -= 1
        anim = Animation(y=self.pos[1] - 34, t='in_out_elastic', duration=.7)
        anim.start(self)
        if self.player:
            actor_anim = Animation(y=self.player.pos[1] - 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.player)
        if self.mod_layer:
            actor_anim = Animation(y=self.mod_layer.pos[1] - 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.mod_layer)
        if self.star:
            actor_anim = Animation(y=self.star.pos[1] - 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.star)
        if self.key:
            actor_anim = Animation(y=self.key.pos[1] - 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.key)
        if self.exit:
            actor_anim = Animation(y=self.exit.pos[1] - 34, t='in_out_elastic', duration=.7)
            actor_anim.start(self.exit)
        if self.portal:
            portal_anim = Animation(y=self.portal.pos[1] - 34, t='in_out_elastic', duration=.7)
            portal_anim.start(self.portal)
        if use_star:
            self.game_map.tile_with_player.player.use_star()