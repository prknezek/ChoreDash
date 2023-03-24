import pygame
import config as cg
from support import import_csv_layout, import_cut_graphics
from tiles import StaticTile, DoorTile
from game_data import *

class Level :
    def __init__(self, level_data, surface) :
        # general setup
        self.display_surface = surface
        self.horizontal_shift = -1
        self.vertical_shift = -1

        self.layouts = {}
        self.sprites = {}

        # import csvs
        for name in house :
            self.layouts[name] = import_csv_layout(level_data[name])
        
        for name in self.layouts :
            print(name)
            self.create_and_add_tile_group_to_list(self.layouts[name], name)

    def create_tile_group(self, layout, type) :
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout) :
            for col_index, val in enumerate(row) :
                if val != '-1' :
                    x = col_index * cg.TILESIZE
                    y = row_index * cg.TILESIZE

                    # create static tile sprites
                    for name in static_tile_paths :
                        if type == name :
                            sprite = self.create_static_sprite(static_tile_paths[name], val, x, y)

                    # create animated tile sprites
                    if type == 'left_doors' :
                        sprite = DoorTile(cg.TILESIZE, x, y, cg.LEFT_DOOR_PATH)
                    if type == 'right_doors' :
                        sprite = DoorTile(cg.TILESIZE, x, y, cg.RIGHT_DOOR_PATH)

                    sprite_group.add(sprite)

        return sprite_group

    def run(self) :
        # run the level
        for sprite in self.sprites :
            self.update_and_draw(self.sprites[sprite]) 

    def create_static_sprite(self, path, val, x, y) :
        tile_list = import_cut_graphics(path)
        tile_surface = tile_list[int(val)]
        sprite = StaticTile(cg.TILESIZE, x, y, tile_surface)
        return sprite

    def create_and_add_tile_group_to_list(self, layout, name) :
        self.sprites[name + '_sprites'] = self.create_tile_group(layout, name)

    def update_and_draw(self, sprites) :
        sprites.update(self.horizontal_shift, self.vertical_shift)
        sprites.draw(self.display_surface)
