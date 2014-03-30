__author__ = 'oddBit'

from kivy.uix.scatterlayout import ScatterLayout
from kivy.animation import Animation
from kivy.clock import Clock
from data.gameData import *
from HexTile import HexTile
from UpDownBubble import UpDownBubble
from random import choice, shuffle, random
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.audio import SoundLoader
from kivy.uix.bubble import Bubble
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from Actor import Actor


def level_diff(from_tile, to_tile):
    if from_tile.row > to_tile.row:
        from_level = from_tile.level + 3
        to_level = to_tile.level
    elif from_tile.row < to_tile.row:
        from_level = from_tile.level
        to_level = to_tile.level + 3
    else:
        from_level = from_tile.level
        to_level = to_tile.level
    return from_level, to_level


class HexScatter(ScatterLayout):
    def __init__(self, hex_tiles, difficulty, soundsOption, musicOption, **kwargs):
        super(HexScatter, self).__init__(**kwargs)
        self.soundsOption = soundsOption
        self.musicOption = musicOption
        self.difficulty = difficulty
        self.x_offset = 1080
        self.y_offset = 1920
        self.hex_tiles = hex_tiles
        self.has_bubble = False
        self.bubble = None
        self.bubble_id = None
        self.selected_hex = None
        self.tiles = []
        self.is_move_mode = False
        self.is_moving = False
        self.from_hex = None
        self.to_hex = None
        self.enemy_turn = False
        self.tile_with_player = None
        self.tile_with_portal = None
        self.is_just_selected = False
        self.move_anim = None
        self.death_anim = None
        self.player_death = False
        self.enemy_death = False
        self.actor_move_data = []
        self.player = None
        self.player_is_jumping = False
        self.player_has_keys = []
        self.player_has_exits = 0
        self.enemy_list = []
        self.skip_turn_bubble = None
        self.score = 0
        self.popup = None
        self.player_won = False
        self.create_map_from_data()

        # for some reason the first time a bubble is loaded, it leads to a one or two second lag, preloading solves this
        self.shadow_bubble = UpDownBubble(pos=(1000, 1000))
        self.add_widget(self.shadow_bubble)
        self.remove_widget(self.shadow_bubble)
        self.hex_tiles = None
        for enemy in self.enemy_list:
            self.add_widget(enemy)

    def create_map_from_data(self):
        tileradius = 120
        for tile in self.hex_tiles:
            if tile.has_land:
                tile_pos = ((tile.col * tileradius + (tileradius / 2) * (tile.row % 2)) + self.x_offset,
                            (tile.row * 95) + tile.row * 102 + tile.level * 34 + self.y_offset)
                hex_tile = HexTile(tile.row, tile.col, tile.type, tile.level, tile.has_actor, tile.has_star,
                                   tile.has_player, tile.key_type, tile.exit_type,
                                   id='hexTile{0}'.format(str(tile.col) + str(tile.row)),
                                   source='assets/graphics/tiles/' + tile.type + '.png',
                                   pos=tile_pos)
                self.tiles.append(hex_tile)
                self.add_widget(hex_tile)
                if tile.has_actor:
                    self.add_actor_to_map(tile, tile_pos)
                hex_tile.post_init()
                if tile.has_portal:
                    self.tile_with_portal = hex_tile
                    self.tile_with_portal.add_portal()
                if tile.has_player:
                    self.tile_with_player = hex_tile
                    self.tile_with_player.add_player()

    def add_actor_to_map(self, tile, tile_pos, add_to_enemy_list=False):
        delay = choice([x / 1000. for x in range(80, 200, 5)])
        actor = Actor(tile.col, tile.row, pos=(tile_pos[0] + 10, tile_pos[1] + 253), anim_delay=delay)
        self.enemy_list.append(actor)
        if add_to_enemy_list:
            self.add_widget(actor)

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.add_widget(tile)

    def move_mode(self, from_hex):
        self.from_hex = from_hex
        self.is_just_selected = True
        Clock.schedule_once(self.set_move_mode, 0.08)

    def set_move_mode(self, dt):
        if self.from_hex.player and not self.enemy_turn:
            self.enemy_turn = True
            self.is_move_mode = True
            self.is_just_selected = False
            self.from_hex.player.select_player()
            self.skip_turn_bubble = SkipTurnBubble(self, pos=(self.from_hex.x + 36, self.from_hex.y + 360))
            self.add_widget(self.skip_turn_bubble)

    def check_proximity(self, to_hex):
        from_col = self.from_hex.col
        from_row = self.from_hex.row
        to_col = to_hex.col
        to_row = to_hex.row
        vector = [from_col - to_col, from_row - to_row]
        if from_row & 1:
            if vector in odd_directions:
                return False
            else:
                return True
        else:
            if vector in even_directions:
                return False
            else:
                return True

    def schedule_move_to_hex(self, to_hex):
        self.to_hex = to_hex
        Clock.schedule_once(self.move_to_hex_prep)

    def move_to_hex_prep(self, dt):
        self.remove_skip_turn()
        self.player_death = False
        self.enemy_death = False
        self.death_anim = Animation(y=self.to_hex.pos[1] + 500, duration=0.3)
        from_level, to_level = level_diff(self.from_hex, self.to_hex)
        if abs(to_level - from_level) > 1 or self.check_proximity(self.to_hex):
            self.end_without_movement(no_move=True, show_too_far=True)
            return
        elif to_level - from_level == 1:
            if self.to_hex.actor:
                self.player_death = True
            self.move_anim = Animation(x=self.to_hex.pos[0] + 10, duration=0.1)
            self.move_anim &= Animation(y=self.to_hex.pos[1] + 279, t='out_back', duration=0.3)
            jump = True
        elif to_level - from_level == -1:
            if self.to_hex.actor:
                self.enemy_death = True
            self.move_anim = Animation(x=self.to_hex.pos[0] + 10, duration=0.1)
            self.move_anim &= Animation(y=self.to_hex.pos[1] + 279, t='out_back', duration=0.3)
            jump = True
        else:
            if self.to_hex.actor:
                self.player_death = True
            jump = False
            self.move_anim = Animation(x=self.to_hex.pos[0] + 10, y=self.to_hex.pos[1] + 279, duration=0.5)
        self.is_moving = True

        if jump:
            self.player_is_jumping = True
        else:
            self.player_is_jumping = False
        if not self.is_move_mode:
            return
        self.player = self.from_hex.player
        self.from_hex.remove_player()
        self.add_widget(self.player)

        self.complete_player_movement(jump)

    def complete_player_movement(self, jump):
        if self.from_hex.col > self.to_hex.col or (self.from_hex.col >= self.to_hex.col and self.from_hex.row % 2):
            if jump:
                self.player.jump_left()
            else:
                self.player.move_left()
        else:
            if jump:
                self.player.jump_right()
            else:
                self.player.move_right()

        self.move_anim.start(self.player)
        if jump:
            jump_sound = SoundLoader.load('assets/audio/player_jump.ogg')
            jump_sound.play()
        else:
            if self.soundsOption:
                walk_sound = SoundLoader.load('assets/audio/player_walk.ogg')
                walk_sound.play()
        self.move_anim.bind(on_complete=self.end_with_player_transfer)
        if self.player_death:
            pass
        elif self.enemy_death:
            self.score += 5 * self.difficulty
            self.parent.counter.update_counter(0, 5 * self.difficulty)
            actor = self.get_enemy_by_tile(self.to_hex.row, self.to_hex.col)
            self.death_anim.start(actor)
            if self.soundsOption:
                enemy_death_sound = SoundLoader.load('assets/audio/enemy_death.ogg')
                enemy_death_sound.play()
            self.to_hex.remove_actor()
            for enemy in self.enemy_list:
                if enemy == actor:
                    self.enemy_list.pop(self.enemy_list.index(enemy))
                    break
            self.death_anim.bind(on_complete=self.remove_enemy)

    def remove_enemy(self, a, b):
        self.remove_widget(b)

    def remove_skip_turn(self):
        if self.skip_turn_bubble:
            self.remove_widget(self.skip_turn_bubble)
            self.skip_turn_bubble = None

    def player_remove_on_death(self, a, b):
        self.tile_with_player.remove_player()

    def move_portal(self):
        self.selected_hex = self.tile_with_portal
        if self.tile_with_portal.level == MAX_LEVEL:
            self.move_hex_down(False)
        elif self.tile_with_portal.level == 0:
            self.move_hex_up(False)
        else:
            self.move_hex_up(False) if random() > 0.5 else self.move_hex_down(False)

    def spawn_enemy_on_portal(self):
        if not self.tile_with_portal.actor:
            self.tile_with_portal.add_actor()
            Clock.schedule_once(self.add_actor_to_portal, 0.7)

    def add_actor_to_portal(self, dt):
        self.add_actor_to_map(self.tile_with_portal, self.tile_with_portal.pos, True)
        if self.tile_with_portal.player:
            self.player_death = True
            self.complete_level()

    def handle_portal(self):
        if self.tile_with_portal:
            self.move_portal()
            if not self.tile_with_portal.actor and random() > 0.2:
                self.spawn_enemy_on_portal()

    def is_player_dead(self):
        if self.player_death:
            self.tile_with_player.player.player_dead()
            death_anim = Animation(x=self.tile_with_player.player.y + 500, duration=0.1)
            death_anim.start(self.tile_with_player.player)
            death_anim.bind(on_complete=self.player_remove_on_death)
            self.player_death = True
            self.complete_level()
            return True

    def handle_star(self):
        if self.tile_with_player.star:
            self.score += 1 * self.difficulty
            self.parent.counter.update_counter(1, 1 * self.difficulty)
            if self.soundsOption:
                pick_star_sound = SoundLoader.load('assets/audio/pick_star.ogg')
                pick_star_sound.play()
            star_anim = Animation(x=self.tile_with_player.star.x,
                                  y=self.tile_with_player.star.y + 80,
                                  duration=0.15)
            star_anim.start(self.tile_with_player.star)
            star_anim.bind(on_complete=self.tile_with_player.remove_star)
            self.tile_with_player.player.add_star()

    def handle_key(self):
        if self.tile_with_player.key:
            self.score += 5 * self.difficulty
            self.parent.counter.update_counter(0, 5 * self.difficulty)
            self.player_has_keys.append(self.tile_with_player.key_type)
            key_anim = Animation(x=self.tile_with_player.key.x,
                                 y=self.tile_with_player.key.y + 80,
                                 duration=0.15)
            key_anim.start(self.tile_with_player.key)
            key_id = self.tile_with_player.key_type
            if key_id == 'keyYellow':
                self.parent.star_counter.ids.keyYellow.source = key_sources[self.tile_with_player.key_type]
                self.parent.star_counter.ids.keyYellow.reload()
            elif key_id == 'keyGreen':
                self.parent.star_counter.ids.keyGreen.source = key_sources[self.tile_with_player.key_type]
                self.parent.star_counter.ids.keyGreen.reload()
            elif key_id == 'keyOrange':
                self.parent.star_counter.ids.keyOrange.source = key_sources[self.tile_with_player.key_type]
                self.parent.star_counter.ids.keyOrange.reload()
            elif key_id == 'keyBlue':
                self.parent.star_counter.ids.keyBlue.source = key_sources[self.tile_with_player.key_type]
                self.parent.star_counter.ids.keyBlue.reload()
            key_anim.bind(on_complete=self.tile_with_player.remove_key)
            if self.soundsOption:
                pick_key_sound = SoundLoader.load('assets/audio/pick_key.ogg')
                pick_key_sound.play()

    def player_has_all_exits(self):
        if self.tile_with_player.exit:
            self.score += 10 * self.difficulty
            self.parent.counter.update_counter(0, 10 * self.difficulty)
            for key in self.player_has_keys:
                if self.tile_with_player.exit_type == key_exit[key]:
                    self.player_has_exits += 1
                    exit_anim = Animation(x=self.tile_with_player.exit.x,
                                          y=self.tile_with_player.exit.y + 80,
                                          duration=0.15)
                    exit_anim.start(self.tile_with_player.exit)
                    exit_anim.bind(on_complete=self.tile_with_player.remove_exit)
                    if self.tile_with_player.exit_type == 'lockYellow':
                        self.parent.star_counter.ids.keyYellow.source = lock_sources[self.tile_with_player.exit_type]
                        self.parent.star_counter.ids.keyYellow.reload()
                    if self.tile_with_player.exit_type == 'lockGreen':
                        self.parent.star_counter.ids.keyGreen.source = lock_sources[self.tile_with_player.exit_type]
                        self.parent.star_counter.ids.keyGreen.reload()
                    if self.tile_with_player.exit_type == 'lockBlue':
                        self.parent.star_counter.ids.keyBlue.source = lock_sources[self.tile_with_player.exit_type]
                        self.parent.star_counter.ids.keyBlue.reload()
                    elif self.tile_with_player.exit_type == 'lockOrange':
                        self.parent.star_counter.ids.keyOrange.source = lock_sources[self.tile_with_player.exit_type]
                        self.parent.star_counter.ids.keyOrange.reload()
                    if len(self.player_has_keys) == self.difficulty and self.player_has_exits == self.difficulty:
                        self.player_won = True
                        self.complete_level()
                        return True

    def end_player_turn(self):
        self.end_without_movement()
        self.handle_portal()
        if self.is_player_dead():
            return
        self.handle_star()
        self.handle_key()
        if self.player_has_all_exits():
            return
        self.player_is_jumping = False
        self.parent.show_enemy_turn_splash()
        Clock.schedule_once(self.process_enemy_turn, 0.7)

    def complete_level(self):
        self.show_reload_popup(True)

    def get_tile_by_row_col(self, row, col):
        for tile in self.tiles:
            if tile.row == row and tile.col == col:
                return tile

    def get_enemy_by_tile(self, row, col):
        for enemy in self.enemy_list:
            if enemy.col == col and enemy.row == row:
                return enemy
        return

    def get_neighbouring_tiles(self, tile):
        n_tiles = []
        if tile.row & 1:
            lookup = even_directions
        else:
            lookup = odd_directions
        for i in lookup:
            n_tile = self.get_tile_by_row_col(tile.row + i[1], tile.col + i[0])
            if n_tile:
                from_level, to_level = level_diff(tile, n_tile)
                if not n_tile.actor and not n_tile.occupied and not abs(from_level - to_level) > 1 and self.get_enemy_by_tile(tile.row, tile.col):
                    if abs(from_level - to_level) == 1 and not self.get_enemy_by_tile(tile.row, tile.col).can_fly:
                        continue
                    else:
                        n_tiles.append(n_tile)

        return n_tiles

    def prepare_actor_move_data(self):
        for tile in self.tiles:
            if tile.actor:
                for e in self.enemy_list:
                    if e.col == tile.col and e.row == tile.row:
                        enemy = e
                        break
                if not enemy.ended_turn:
                    n_tiles = self.get_neighbouring_tiles(tile)
                    if n_tiles:
                        self.from_hex = tile
                        for t in n_tiles:
                            if t.player:
                                tile_choice = t
                                self.player_death = True
                                break
                            else:
                                tile_choice = choice(n_tiles)
                        tile_choice.occupied = True
                        self.actor_move_data.append((tile, enemy, tile_choice))
                        tile.remove_actor()

    def process_actor_movement(self):
        for data in self.actor_move_data:
            tile = data[0]
            actor = data[1]
            to_hex = data[2]
            if tile.col > to_hex.col or (tile.col >= to_hex.col and tile.row % 2):
                actor.move_left()
            else:
                actor.move_right()
            from_level, to_level = level_diff(tile, to_hex)
            if abs(from_level - to_level) == 1:
                move_anim = Animation(x=to_hex.pos[0] + 10, duration=0.1)
                move_anim &= Animation(y=to_hex.pos[1] + 249, t='out_back', duration=0.2)
            else:
                move_anim = Animation(x=to_hex.pos[0] + 10, y=to_hex.pos[1] + 249, duration=0.2)
            move_anim.start(actor)

    def process_enemy_turn(self, dt):
        shuffle(self.enemy_list)
        self.is_moving = True
        self.is_move_mode = True
        self.prepare_actor_move_data()
        self.process_actor_movement()

        if self.actor_move_data:
            Clock.schedule_once(self.end_enemy_turn, 0.4)
        else:
            self.end_enemy_turn(0)

    def end_enemy_turn(self, dt):
        for data in self.actor_move_data:
            data[2].add_actor()
            data[1].col = data[2].col
            data[1].row = data[2].row
        for enemy in self.enemy_list:
            enemy.ended_turn = False
        for tile in self.tiles:
            if tile.actor:
                tile.occupied = True
            else:
                tile.occupied = False
        self.is_move_mode = False
        self.is_moving = False
        self.actor_move_data = []
        if self.player_death:
            self.complete_level()
        self.enemy_turn = False
        self.parent.remove_enemy_turn_splash()

    def end_without_movement(self, no_move=False, show_too_far=False):
        self.is_move_mode = False
        self.is_moving = False
        if self.tile_with_player.player:
            self.tile_with_player.player.stop_player()
        self.remove_skip_turn()
        if no_move:
            self.enemy_turn = False
        if show_too_far:
            self.parent.show_too_far_splash()
            Clock.schedule_once(self.parent.remove_tile_too_far_splash, 0.6)

    def end_with_player_transfer(self, a, b):
        self.to_hex.add_player(self.player.stars, self.player.pos)
        self.is_move_mode = False
        self.is_moving = False
        self.to_hex.player.stop_player()
        self.tile_with_player = self.to_hex
        self.remove_widget(self.player)
        self.player = None
        self.end_player_turn()

    def add_bubble(self, pos, id, hex):
        if not self.bubble:
            bubble_pos = [pos[0], pos[1] + 344]
            self.selected_hex = hex
            if self.selected_hex.level == MAX_LEVEL:
                up_disabled = True
            else:
                up_disabled = False
            if self.selected_hex.level == 0:
                down_disabled = True
            else:
                down_disabled = False
            self.bubble = UpDownBubble(up_disabled, down_disabled, pos=bubble_pos)
            self.add_widget(self.bubble)
            self.has_bubble = True
            self.bubble_id = id

    def remove_bubble(self, id):
        if self.bubble and id == self.bubble_id:
            self.remove_widget(self.bubble)
            self.bubble = None
            self.selected_hex = None
            self.enemy_turn = False
            Clock.schedule_once(self.clear_bubble, 0.1)

    def move_hex_up(self, use_star=True):
        if self.tile_with_player.player.stars > 0:
            self.selected_hex.move_up(use_star)
            for enemy in self.enemy_list:
                if self.selected_hex.actor and enemy.col == self.selected_hex.col and enemy.row == self.selected_hex.row:
                    actor_anim = Animation(y=enemy.pos[1] + 34, t='in_out_elastic', duration=.7)
                    actor_anim.start(enemy)
                    break
            if use_star:
                self.parent.counter.update_counter(-1)

    def move_hex_down(self, use_star=True):
        if self.tile_with_player.player.stars > 0:
            self.selected_hex.move_down(use_star)
            for enemy in self.enemy_list:
                if self.selected_hex.actor and enemy.col == self.selected_hex.col and enemy.row == self.selected_hex.row:
                    actor_anim = Animation(y=enemy.pos[1] - 34, t='in_out_elastic', duration=.7)
                    actor_anim.start(enemy)
                    break
            if use_star:
                self.parent.counter.update_counter(-1)

    def clear_bubble(self, dt):
        self.has_bubble = False

    def show_reload_popup(self, death_or_victory=False):
        new_difficulty = choice([1,2,3,4])
        self.popup = ReloadPopup(self, death_or_victory, new_difficulty, self.player_won)
        self.popup.open()


class ReloadPopup(Popup):
    player_death = BooleanProperty(False)
    player_won = BooleanProperty(False)

    def __init__(self, context, player_death, new_difficulty, player_won, **kwargs):
        super(ReloadPopup, self).__init__(**kwargs)
        self.image = 'assets/graphics/ui/popupImg.png'
        self.context = context
        self.player_death = player_death
        self.player_won = player_won
        self.new_difficulty = new_difficulty


class StarCounter(BoxLayout):
    stars = NumericProperty(0)
    score = NumericProperty(0)

    def __init__(self, stars, score=0, **kwargs):
        super(StarCounter, self).__init__(**kwargs)
        self.stars = stars
        self.score = score

    def update_counter(self, stars, score=0):
        self.stars += stars
        self.score += score


class SkipTurnBubble(Bubble):
    def __init__(self, context, **kwargs):
        super(SkipTurnBubble, self).__init__(**kwargs)
        self.context = context