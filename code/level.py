import pygame
import config as cg
from support import import_csv_layout, import_cut_graphics
from tiles import StaticTile, DoorTile
from game_data import *
from player import Player

class Level :
    def __init__(self, level_data, surface) :
        # general setup
        self.display_surface = surface
        self.horizontal_shift = 0
        self.vertical_shift = 0

        self.layouts = {}
        self.sprites = {}

        self.player = pygame.sprite.GroupSingle()

        # import csvs
        for name in house :
            if name != 'player' :
                self.layouts[name + '_layout'] = import_csv_layout(level_data[name])
            else :
                self.player_setup()

        for name in self.layouts :
            self.create_and_add_tile_group_to_list(self.layouts[name], name[:-7])

    def player_setup(self) :
        player_sprite = Player(((cg.WIN_WIDTH / 2) - (cg.TILESIZE / 2), (cg.WIN_HEIGHT / 2)- (cg.TILESIZE / 2)))
        self.player.add(player_sprite)

    def create_and_add_tile_group_to_list(self, layout, name) :
        self.sprites[name + '_sprites'] = self.create_tile_group(layout, name)

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
                    if type == 'doors' :
                        sprite = DoorTile(cg.TILESIZE, x, y, cg.RIGHT_DOOR_PATH, cg.DOOR_TILE_OFFSET)
                        # when setting door to open to left, offset by 24
                        # sprite.offset_x(24)
                        # sprite.set_open_animation(cg.LEFT_DOOR_PATH)

                    sprite_group.add(sprite)

        return sprite_group

    def create_static_sprite(self, path, val, x, y) :
        tile_list = import_cut_graphics(path)
        tile_surface = tile_list[int(val)]
        sprite = StaticTile(cg.TILESIZE, x, y, tile_surface)
        return sprite
    
    def run(self, dt) :
        # run the level
        for sprite in self.sprites :
            # furthest back drawn first
            self.update_and_draw(self.sprites[sprite])
            # if sprite != 'constraints_sprites':
            #     self.update_and_draw(self.sprites[sprite])
            # else :
            #     self.sprites[sprite].update(self.horizontal_shift, self.vertical_shift)
        # "camera" movement
        self.scroll()

        # player
        self.player.update(dt)
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)

    def update_and_draw(self, sprites) :
        sprites.update(self.horizontal_shift, self.vertical_shift)
        sprites.draw(self.display_surface)

    def scroll(self) :
        player = self.player.sprite

        direction_x = player.direction.x
        direction_y = player.direction.y

        if direction_x < 0 :
            self.horizontal_shift = cg.PLAYER_SPEED
        elif direction_x > 0:
            self.horizontal_shift = -cg.PLAYER_SPEED
        else :
            self.horizontal_shift = 0

        if direction_y < 0 :
            self.vertical_shift = cg.PLAYER_SPEED
        elif direction_y > 0 :
            self.vertical_shift = -cg.PLAYER_SPEED
        else :
            self.vertical_shift = 0
    
    def horizontal_movement_collision(self) :
        player = self.player.sprite

        for sprite in self.sprites :
            if sprite == 'constraints_sprites' :
                for tile in self.sprites[sprite].sprites() :
                    if tile.rect.colliderect(player.rect) :
                        print("collision")