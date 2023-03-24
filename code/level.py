import pygame
import config as cg
from support import import_csv_layout, import_cut_graphics
from tiles import StaticTile, DoorTile

class Level :
    def __init__(self, level_data, surface) :
        # general setup
        self.display_surface = surface
        self.horizontal_shift = -1
        self.vertical_shift = -1

        # black
        black_layout = import_csv_layout(level_data['black'])
        self.black_sprites = self.create_tile_group(black_layout, 'black')

        # floor
        floor_layout = import_csv_layout(level_data['floor'])
        self.floor_sprites = self.create_tile_group(floor_layout, 'floor')

        # furniture
        wall_layout = import_csv_layout(level_data['walls'])
        self.wall_sprites = self.create_tile_group(wall_layout, 'walls')

        # left door
        left_door_layout = import_csv_layout(level_data['left_doors'])
        self.left_door_sprites = self.create_tile_group(left_door_layout, 'left_doors')

        # right door
        right_door_layout = import_csv_layout(level_data['right_doors'])
        self.right_door_sprites = self.create_tile_group(right_door_layout, 'right_doors')

        # bathroom decoration
        bathroom_decoration_layout = import_csv_layout(level_data['bathroom_decoration'])
        self.bathroom_decoration_sprites = self.create_tile_group(bathroom_decoration_layout, 'bathroom_decoration')

    def create_tile_group(self, layout, type) :
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout) :
            for col_index, val in enumerate(row) :
                if val != '-1' :
                    x = col_index * cg.TILESIZE
                    y = row_index * cg.TILESIZE

                    if type == 'black' :
                        black_tile_list = import_cut_graphics(cg.BLACK_TILE_PATH)
                        tile_surface = black_tile_list[int(val)]
                        sprite = StaticTile(cg.TILESIZE, x, y, tile_surface)
                        
                    if type == 'floor' :
                        floor_tile_list = import_cut_graphics(cg.FLOOR_TILE_PATH)
                        tile_surface = floor_tile_list[int(val)]
                        sprite = StaticTile(cg.TILESIZE, x, y, tile_surface)
                    
                    if type == 'walls' :
                        wall_tile_list = import_cut_graphics(cg.WALL_TILE_PATH)
                        tile_surface = wall_tile_list[int(val)]
                        sprite = StaticTile(cg.TILESIZE, x, y, tile_surface)

                    if type == 'bathroom_decoration' :
                        bathroom_decoration_tile_list = import_cut_graphics(cg.BATHROOM_DECORATION_PATH)
                        tile_surface = bathroom_decoration_tile_list[int(val)]
                        sprite = StaticTile(cg.TILESIZE, x, y, tile_surface)

                    if type == 'left_doors' :
                        sprite = DoorTile(cg.TILESIZE, x, y, cg.LEFT_DOOR_PATH)

                    if type == 'right_doors' :
                        sprite = DoorTile(cg.TILESIZE, x, y, cg.RIGHT_DOOR_PATH)

                    sprite_group.add(sprite)

        return sprite_group

    def run(self) :
        # run the level

        # black
        self.black_sprites.update(self.horizontal_shift, self.vertical_shift)
        self.black_sprites.draw(self.display_surface)

        # floor
        self.floor_sprites.update(self.horizontal_shift, self.vertical_shift)
        self.floor_sprites.draw(self.display_surface)

        # walls
        self.wall_sprites.update(self.horizontal_shift, self.vertical_shift)
        self.wall_sprites.draw(self.display_surface)

        # left doors
        self.left_door_sprites.update(self.horizontal_shift, self.vertical_shift)
        self.left_door_sprites.draw(self.display_surface)

        # right doors
        self.right_door_sprites.update(self.horizontal_shift, self.vertical_shift)
        self.right_door_sprites.draw(self.display_surface)

        # bathroom decoration
        self.bathroom_decoration_sprites.update(self.horizontal_shift, self.vertical_shift)
        self.bathroom_decoration_sprites.draw(self.display_surface)
