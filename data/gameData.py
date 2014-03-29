__author__ = 'oddBit'

from Enum import Enum

tiles = ('tileAutumn', 'tileDirt', 'tileGrass', 'tileLava', 'tileMagic', 'tileRock', 'tileSand', 'tileSnow', 'tileSnow',
         'tileStone', 'tileWater')

mod_layers = ('overlay01', 'overlay02', 'overlay03', 'overlay04', 'overlay05', 'overlay06')

enemies = ('blob', 'spider', 'fly')

even_directions = ([1, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [0, 1])
odd_directions = ([0, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1])

key_exit = {'keyBlue': 'lockBlue', 'keyGreen': 'lockGreen', 'keyOrange': 'lockOrange', 'keyYellow': 'lockYellow'}

key_sources = {'keyBlue': 'assets/graphics/tiles/keyBlue.png', 'keyGreen': 'assets/graphics/tiles/keyGreen.png',
               'keyOrange': 'assets/graphics/tiles/keyOrange.png', 'keyYellow': 'assets/graphics/tiles/keyYellow.png'}

lock_sources = {'lockBlue': 'assets/graphics/tiles/lockBlue.png', 'lockGreen': 'assets/graphics/tiles/lockGreen.png',
                'lockOrange': 'assets/graphics/tiles/lockOrange.png',
                'lockYellow': 'assets/graphics/tiles/lockYellow.png'}

flyables = 'fly'

map_sizes = ((6, 7), (7, 8), (7, 8), (8, 9))

PlayerStates = Enum(
    ['SIT_LEFT', 'SIT_RIGHT', 'SIT_LEFT_SELECTED', 'SIT_RIGHT_SELECTED', 'JUMP_LEFT', 'JUMP_RIGHT', 'WALK_LEFT',
     'WALK_RIGHT', 'DEAD'])

ActorStated = Enum(['SIT_LEFT', 'SIT_RIGHT', 'JUMP_LEFT', 'JUMP_RIGHT', 'WALK_LEFT', 'WALK_RIGHT', 'DEAD'])

player_sprites = {'SIT_LEFT': 'assets/graphics/player/playerStandLeft.png',
                  'SIT_RIGHT': 'assets/graphics/player/playerStandRight.png',
                  'SIT_LEFT_SELECTED': 'assets/graphics/player/playerStandLeftSelected.png',
                  'SIT_RIGHT_SELECTED': 'assets/graphics/player/playerStandRightSelected.png',
                  'JUMP_LEFT': 'assets/graphics/player/playerJumpLeft.png',
                  'JUMP_RIGHT': 'assets/graphics/player/playerJumpRight.png',
                  'WALK_LEFT': 'assets/graphics/player/playerWalkLeft.zip',
                  'WALK_RIGHT': 'assets/graphics/player/playerWalkRight.zip',
                  'DEAD': 'assets/graphics/player/playerDeath.png'}

help_screens = ['tileselect', 'stars', 'playerselect', 'movement', 'killenemies', 'goal', 'portal']

MAX_LEVEL = 3
TREE_POS = ((30, 115), (30, 75), (50, 65))
FLOWER_POS = (((-15, 80), (15, 45), (35, 65)), ((-25, 60), (15, 85), (-5, 75)), ((45, 60), (25, 55), (35, 85)),
              ((45, 60), (30, 65), (-25, 55)))
STAR_POS = (-20, 90)