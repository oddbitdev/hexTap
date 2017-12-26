#!/usr/bin/python
# encoding: utf-8

__author__ = 'oddBit'

import kivy

kivy.require('1.8.0')
from kivy.app import App
from kivy.lang import Builder
from MapCanvas import MapCanvas
from MainMenu import MainMenu
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from SettingsJson import settings_json
from kivy.core.audio import SoundLoader
from HelpMenu import HelpMenu
from kivy.utils import platform
from data.gameData import *

try:
    from revmob import RevMob as revmob
    use_ads = True
except ImportError:
    use_ads = False

Builder.load_file('gameScreen.kv')
Builder.load_file('mainMenu.kv')

if use_ads:
    if platform() == 'android':
        REVMOB_APP_ID = 'android_id'
    elif platform() == 'ios':
        REVMOB_APP_ID = 'ios_id'
    else:
        REVMOB_APP_ID = 'unknown platform for RevMob'

    revmob.start_session(REVMOB_APP_ID)


class HexTap(App):
    def __init__(self, **kwargs):
        super(HexTap, self).__init__(**kwargs)
        self.difficulty = 1
        self.first_run = True
        self.current_state = 'mainMenu'
        self.content = BoxLayout()
        self.main_menu = MainMenu()
        self.help_menu = HelpMenu()
        self.game_map = None
        self.content.add_widget(self.main_menu)
        self.music = SoundLoader.load('assets/audio/music.ogg')
        self.soundsOption = True
        self.musicOption = False
        self.hardcoreOption = False

    def safe_options_loading(self):
        if type(self.soundsOption) == bool or type(self.soundsOption) == int:
            pass
        elif self.soundsOption == 'True' or '1' in self.soundsOption:
            self.soundsOption = True
        else:
            self.soundsOption = False
        if type(self.musicOption) == bool or type(self.musicOption) == int:
            pass
        elif self.musicOption == 'True' or '1' in self.musicOption:
            self.musicOption = True
        else:
            self.musicOption = False
        if type(self.hardcoreOption) == bool or type(self.hardcoreOption) == int:
            pass
        elif self.hardcoreOption == 'True' or '1' in self.hardcoreOption:
            self.hardcoreOption = True
        else:
            self.hardcoreOption = False

    def build(self):
        self.use_kivy_settings = False
        self.soundsOption = self.config.get('sound', 'soundsOption')
        self.musicOption = self.config.get('sound', 'musicOption')
        self.hardcoreOption = self.config.get('game', 'hardcoreOption')
        self.safe_options_loading()
        Clock.schedule_interval(self.update, 1. / 1.5)
        return self.content

    def show_help(self):
        self.content.clear_widgets()
        self.content.add_widget(self.help_menu)

    def generate_main_menu(self):
        self.content.clear_widgets()
        self.content.add_widget(self.main_menu)

    def new_game(self):
        if use_ads:
            revmob.show_popup()
        self.content.clear_widgets()
        self.content.add_widget(Image(source='assets/graphics/ui/loading.png', size=Window.size, allow_stretch=True))
        Clock.schedule_once(self.post_splash)

    def post_splash(self, dt):
        rows, cols = map_sizes[self.difficulty-1]
        self.game_map = MapCanvas(cols, rows, self.difficulty, self.hardcoreOption, self.soundsOption,
                                  self.musicOption)
        self.content.clear_widgets()
        self.content.add_widget(self.game_map)

    def update(self, dt):
        if self.main_menu.start_game:
            self.new_game()
            self.main_menu.start_game = False
        if self.main_menu.show_help:
            self.show_help()
            self.main_menu.show_help = False
        if self.help_menu.back_to_main:
            self.generate_main_menu()
            self.help_menu.back_to_main = False
        if self.game_map and self.game_map.return_to_menu:
            self.generate_main_menu()
            self.game_map.return_to_menu = False
        if self.musicOption and self.music.state == 'stop':
            self.music.play()
        elif not self.musicOption and self.music.state == 'play':
            self.music.stop()

    def build_config(self, config):
        try:
            config.setdefaults('sound', {
                'musicOption': '0',
                'soundsOption': '1'
            })
            config.setdefaults('game', {
                'hardcoreOption': '0'
            })
        except TypeError:
            config.setdefaults('sound', {
                'musicOption': False,
                'soundsOption': True
            })
            config.setdefaults('game', {
                'hardcoreOption': False
            })

    def build_settings(self, settings):
        settings.add_json_panel('hexTap options', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if key == 'musicOption':
            if type(value) == bool or type(value) == int:
                self.musicOption = value
            elif value == 'True' or '1' in value:
                self.musicOption = True
            else:
                self.musicOption = False
        elif key == 'soundsOption':
            if type(value) == bool or type(value) == int:
                self.soundsOption = value
            elif value == 'True' or '1' in value:
                self.soundsOption = True
            else:
                self.soundsOption = False
        elif key == 'hardcoreOption':
            if type(value) == bool or type(value) == int:
                self.hardcoreOption = value
            elif value == 'True' or '1' in value:
                self.hardcoreOption = True
            else:
                self.hardcoreOption = False

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    HexTap().run()
