__author__ = 'oddBit'

from kivy.uix.bubble import Bubble
from kivy.properties import BooleanProperty


class UpDownBubble(Bubble):
    up_disabled = BooleanProperty(False)
    down_disabled = BooleanProperty(False)

    def __init__(self, up_disabled=False, down_disabled=False, **kwargs):
        super(UpDownBubble, self).__init__(**kwargs)
        self.up_disabled = up_disabled
        self.down_disabled = down_disabled

    def up(self):
        self.parent.parent.move_hex_up()

    def down(self):
        self.parent.parent.move_hex_down()