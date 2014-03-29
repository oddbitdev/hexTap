__author__ = 'oddBit'

from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.properties import StringProperty
from data.gameData import *


Builder.load_string('''
#:kivy 1.8.0
<Page>
    orientation: 'vertical'
    id: helpPage
    BoxLayout:
        Image:
            source: root.current_image
            allow_stretch: True
            mipmap: False
            keep_ratio: False
            anim_delay: 0.5

<HelpMenu>
    orientation: 'vertical'
    BoxLayout:
        size_hint: 1, 0.95
        HelpMenuCarousel:
            id: carousel
    BoxLayout:
        size_hint: 1.0, 0.05
        Button:
            id: backToMainMenu
            text: 'Back'
            on_release: root.back_to_main_menu()
            background_normal: 'assets/graphics/ui/button_normal.png'
            background_down: 'assets/graphics/ui/button_down.png'
''')


class Page(BoxLayout):
    current_image = StringProperty()

    def __init__(self, **kwargs):
        super(Page, self).__init__(**kwargs)

    def set_current_image(self, image):
        self.current_image = image


class HelpMenuCarousel(Carousel):
    def __init__(self, **kwargs):
        super(HelpMenuCarousel, self).__init__(**kwargs)
        for item in help_screens:
            page = Page()
            page.set_current_image('assets/graphics/ui/' + item + '.png')
            self.add_widget(page)


class HelpMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(HelpMenu, self).__init__(**kwargs)
        self.carousel = self.children[1].children[0]
        self.back_to_main = False

    def back_to_main_menu(self):
        self.back_to_main = True