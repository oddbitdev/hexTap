__author__ = 'oddBit'

import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'game settings'},
    {'type': 'bool',
     'title': 'hardcore mode',
     'desc': 'adds enemies and a portal to the map',
     'section': 'game',
     'key': 'hardcoreOption'},
    {'type': 'title',
     'title': 'sound settings'},
    {'type': 'bool',
     'title': 'play music',
     'desc': '',
     'section': 'sound',
     'key': 'musicOption'},
    {'type': 'bool',
     'title': 'play game sounds',
     'desc': '',
     'section': 'sound',
     'key': 'soundsOption'}
])