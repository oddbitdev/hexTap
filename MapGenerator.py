__author__ = 'oddBit'

from random import choice, random

from data.gameData import *


def get_new_type(current_type):
    if random() > 0.8:
        return choice(tiles)
    else:
        return current_type


class Tile:
    def __init__(self, row, col, has_player, has_land, type, has_star, has_actor, level, key_type, exit_type, portal):
        self.exit_type = exit_type
        self.key_type = key_type
        self.level = level
        self.has_actor = has_actor
        self.has_star = has_star
        self.type = type
        self.col = col
        self.row = row
        self.has_player = has_player
        self.has_land = has_land
        self.has_portal = portal


class MapGenerator:
    def __init__(self, h_tiles, v_tiles):
        self.h_tiles = h_tiles
        self.v_tiles = v_tiles

    def generate_map(self, difficulty, hardcoreOption=False, clone=False):
        hex_tiles = []
        landed_tiles = []
        player_tiles = []
        exit_tiles = []
        key_tiles = []
        for row in reversed(range(self.v_tiles)):
            for col in range(self.h_tiles):
                hex_tiles.append(Tile(row, col, False, True, None, False, False, 0, None, None, False))
        keys_and_exits = []
        i = 0
        for k, v in key_exit.items():
            if i < difficulty:
                keys_and_exits.append((k, v))
                i += 1
        type_choice = choice(tiles)
        for tile in hex_tiles:
            if (tile.col == 0 or tile.col == self.h_tiles - 1) and random() > 0.7:
                tile.has_land = False
            if (tile.row == 0 or tile.row == self.v_tiles - 1) and random() > 0.7:
                tile.has_land = False
            if random() > 0.99 and (3 < tile.col < self.h_tiles - 3) and (3 < tile.row < self.v_tiles - 3):
                tile.has_land = False
            if random() > 0.55:
                pass
            elif random() > 0.6:
                tile.level = 1
            elif random() > 0.8:
                tile.level = 2
            elif random > 0.9:
                tile.level = 3
            if tile.has_land:
                if tile.row <= 1:
                    player_tiles.append(tile)
                else:
                    key_tiles.append(tile)
                if tile.row >= self.v_tiles - 3:
                    exit_tiles.append(tile)

                landed_tiles.append(tile)
                tile.type = type_choice
                type_choice = get_new_type(type_choice)

        player_tile = choice(player_tiles)
        if clone:
            i = player_tiles.index(player_tile)
            player_tiles.pop(i)
            clone_tile = choice(player_tiles)
            clone_tile.has_player = True
            if clone_tile.has_actor:
                clone_tile.has_actor = False
        player_tile.has_player = True

        picked_keys = []
        picked_exits = []
        for k, v in keys_and_exits:
            picked_exit = False
            picked_key = False
            while not picked_exit and not picked_key:
                key = choice(key_tiles)
                exit = choice(exit_tiles)
                if key != exit and exit not in picked_exits and key not in picked_keys and exit not in picked_keys and key not in picked_exits:
                    picked_key = True
                    picked_exit = True
                    picked_keys.append(key)
                    picked_exits.append(exit)
                    key.key_type = k
                    exit.exit_type = v
                    key.has_actor = True
                    exit.has_actor = True
        if hardcoreOption:
            hardMod = 0.15
        else:
            hardMod = 0
        picked_portal = False
        while not picked_portal and hardcoreOption:
            portal_tile = choice(key_tiles)
            if hardcoreOption and not picked_portal and portal_tile.has_land and not portal_tile.has_player and not portal_tile.has_actor and not portal_tile.key_type and not portal_tile.exit_type and portal_tile.row < self.v_tiles - 1:
                portal_tile.has_portal = True
                picked_portal = True
        for tile in hex_tiles:
            if tile.has_land and not tile.has_player and not tile.has_portal:
                if random() > 0.8 - hardMod and tile.row != player_tile.row:
                    tile.has_actor = True
                if random() > 0.5:
                    tile.has_star = True

        return hex_tiles