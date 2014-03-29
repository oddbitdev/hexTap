__author__ = 'oddBit'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.start_game = False
        self.show_help = False

    def show_info(self):
        info = InfoPopup()
        info.open()


class InfoPopup(Popup):
    pass