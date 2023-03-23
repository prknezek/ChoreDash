import pygame
from .config import *
from support import import_csv_layout, import_cut_graphics
from tiles import Tile, StaticTile

class Level :
    def __init__(self, level_data, surface) :
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # black setup
        black_layout = import_csv_layout(level_data['black'])
        self.black_sprites = self.create_tile_group(black_layout, 'black')

        # floor setup
        floor_layout = import_csv_layout(level_data['floor'])
        self.floor_sprites = self.create_tile_group(floor_layout, 'floor')

        # furniture setup
        wall_layout = import_csv_layout(level_data['walls'])
        self.wall_sprites = self.create_tile_group(wall_layout, 'walls')

    def create_tile_group(self, layout, type) :
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout) :
            for col_index, val in enumerate(row) :
                if val != '-1' :
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    if type == 'black' :
                        black_tile_list = import_cut_graphics(BLACK_TILE_PATH)
                        tile_surface = black_tile_list[int(val)]
                        sprite = StaticTile(TILESIZE, x, y, tile_surface)
                        
                    if type == 'floor' :
                        floor_tile_list = import_cut_graphics(FLOOR_TILE_PATH)
                        tile_surface = floor_tile_list[int(val)]
                        sprite = StaticTile(TILESIZE, x, y, tile_surface)
                    
                    if type == 'walls' :
                        wall_tile_list = import_cut_graphics(WALL_TILE_PATH)
                        tile_surface = wall_tile_list[int(val)]
                        sprite = StaticTile(TILESIZE, x, y, tile_surface)


                    sprite_group.add(sprite)

        return sprite_group

    def run(self) :
        # run the level

        # black
        self.black_sprites.draw(self.display_surface)
        self.black_sprites.update(self.world_shift)

        # floor
        self.floor_sprites.draw(self.display_surface)
        self.floor_sprites.update(self.world_shift)

        # walls
        self.wall_sprites.draw(self.display_surface)
        self.wall_sprites.update(self.world_shift)
