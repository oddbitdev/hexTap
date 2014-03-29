__author__ = 'oddBit'

from kivy.uix.floatlayout import FloatLayout

from HexScatter import HexScatter, StarCounter
from MapGenerator import MapGenerator
from kivy.core.window import Window
from kivy.uix.image import Image
from data.gameData import *


class MapCanvas(FloatLayout):
    def __init__(self, cols, rows, difficulty, hardcoreOption, soundsOption, musicOptions, **kwargs):
        super(MapCanvas, self).__init__(**kwargs)
        self.soundsOption = soundsOption
        self.musicOption = musicOptions
        self.hardcore_option = hardcoreOption
        self.tile_map = None
        self.counter = None
        self.map_generator = MapGenerator(cols, rows)
        self.hex_tiles = self.map_generator.generate_map(difficulty, hardcoreOption)
        self.difficulty = difficulty
        tile_map = self.build_map_tiles()
        self.add_tile_map(tile_map)
        self.star_counter = StarCounter(23)
        self.add_counter(self.star_counter)
        self.return_to_menu = False
        self.enemy_turn_splash = None
        self.tile_too_far_splash = None

    def add_tile_map(self, tile_map):
        for tile in tile_map.tiles:
            if tile.player:
                px = tile.player.x
                py = tile.player.y
                break
        self.tile_map = tile_map
        self.tile_map.pos = (-px + Window.size[0] / 2, -py + Window.size[1] / 2)
        self.add_widget(self.tile_map)

    def add_counter(self, counter):
        self.counter = counter
        self.add_widget(self.counter)

    def go_to_main_menu(self):
        self.tile_map.popup.dismiss()
        self.return_to_menu = True

    def reload_level(self, new_map=False, new_difficulty=0):
        if new_difficulty:
            self.difficulty = new_difficulty
        if self.tile_map.popup:
            self.tile_map.popup.dismiss()
        self.clear_widgets()
        self.tile_map = None
        if new_map:
            self.hex_tiles = None
            print new_difficulty
            rows, cols = map_sizes[new_difficulty-1]
            self.map_generator = MapGenerator(cols, rows)
            self.hex_tiles = self.map_generator.generate_map(self.difficulty, self.hardcore_option)
        tile_map = self.build_map_tiles()
        self.add_tile_map(tile_map)
        self.star_counter = StarCounter(23)
        self.add_counter(self.star_counter)

    def show_enemy_turn_splash(self):
        self.enemy_turn_splash = Image(source='assets/graphics/ui/enemyTurn.png', size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.enemy_turn_splash)

    def remove_enemy_turn_splash(self):
        if self.enemy_turn_splash:
            self.remove_widget(self.enemy_turn_splash)

    def show_too_far_splash(self):
        self.tile_too_far_splash = Image(source='assets/graphics/ui/tileTooFar.png', size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.tile_too_far_splash)

    def remove_tile_too_far_splash(self, dt):
        if self.tile_too_far_splash:
            self.remove_widget(self.tile_too_far_splash)

    def build_map_tiles(self):
        return HexScatter(self.hex_tiles, self.difficulty, self.soundsOption, self.musicOption,
                          size=[18 * 120 + 1080, 22 * 120 + 1920], pos=[0, 0],
                          auto_bring_to_front=False)