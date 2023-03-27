import pygame
import config as cg
from player import Player
from sprites import Generic, Door, Constraint, Trashcan, InteractButton
from pytmx.util_pygame import load_pygame
from support import *

class Level :
    def __init__(self) :
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()

        self.collision_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.trashcan_sprites = pygame.sprite.Group()
        self.interact_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self) :
        tmx_data = load_pygame('./house/house_data/house.tmx')

        # draw generic tiles
        self.draw_generic_tiles('Constraints', 'constraints')
        self.draw_generic_tiles('Black', 'black')
        self.draw_generic_tiles('Floor', 'floor')
        self.draw_generic_tiles('FloorDecoration', 'floor_decoration')
        self.draw_generic_tiles('Walls', 'walls')
        self.draw_generic_tiles('WallDecoration', 'wall_decoration')
        self.draw_generic_tiles('Furniture', 'furniture')
        self.draw_generic_tiles_in_layer(cg.DECORATION, 'decoration')
        self.draw_generic_tiles('InFront', 'in_front')
        self.draw_generic_tiles('InFrontDecoration', 'in_front_decoration')

        # draw interact buttons
        for obj in tmx_data.get_layer_by_name('InteractButtons') :
            InteractButton((int(obj.x), int(obj.y)), obj.name, self.display_surface, [self.all_sprites, self.interact_sprites])

        # draw trashcans
        for x, y, surface in tmx_data.get_layer_by_name('Trashcans').tiles() :
            color = ''

            if x == 9 :
                color = 'green'
            elif x == 15 :
                color = 'white'
            elif x == 12 :
                color = 'blue'
            elif x == 30 :
                color = 'pink'

            if (x, y) in [(9, 6), (15, 6), (12, 11), (30, 13)] :
                Trashcan(pos = (x * cg.TILESIZE, y * cg.TILESIZE),
                        surface = surface,
                        groups = [self.all_sprites, self.trashcan_sprites],
                        player_sprite = self.player_sprite,
                        color = color,
                        interact_sprites = self.interact_sprites)
        
        # draw door tiles
        door_frames = import_folder('./graphics/animated_tiles/right_door')

        for x, y, surface in tmx_data.get_layer_by_name('Doors').tiles() :
            Door(pos = (x * cg.TILESIZE, y * cg.TILESIZE),
                 frames = door_frames,
                 groups = [self.all_sprites, self.collision_sprites, self.door_sprites],
                 offset = cg.DOOR_TILE_OFFSET,
                 player_sprite = self.player_sprite)

        # draw player
        for obj in tmx_data.get_layer_by_name('Player') :
            if obj.name == 'Start' :
                self.player = Player((obj.x, obj.y), [self.all_sprites, self.player_sprite], self.collision_sprites, self.door_sprites)
        
    def run(self, dt) :
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.event_detection()

    def event_detection(self) :
        empty_count = 0

        for sprite in self.trashcan_sprites :
            if sprite.is_empty :
                empty_count += 1
        
        if empty_count == 4 :
            print('all trashcans empty')

    def draw_generic_tiles(self, tiled_name, layer_name) :
        tmx_data = load_pygame('./house/house_data/house.tmx')
        for x, y, surface in tmx_data.get_layer_by_name(tiled_name).tiles() :
            if tiled_name != 'Constraints' :
                Generic((x * cg.TILESIZE, y * cg.TILESIZE), surface, self.all_sprites, cg.LAYERS[layer_name])
            else :
                Constraint((x * cg.TILESIZE, y * cg.TILESIZE), pygame.Surface((cg.TILESIZE, cg.TILESIZE)), self.collision_sprites)
    
    def draw_generic_tiles_in_layer(self, tiled_layer, layer_name) :
        tmx_data = load_pygame('./house/house_data/house.tmx')
        for layer in tiled_layer :
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles() :
                Generic((x * cg.TILESIZE, y * cg.TILESIZE), surface, self.all_sprites, cg.LAYERS[layer_name])

class CameraGroup(pygame.sprite.Group) :
    def __init__(self) :
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player) :
        self.offset.x = player.rect.centerx - cg.SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - cg.SCREEN_HEIGHT / 2

        for layer in cg.LAYERS.values() :
            for sprite in self.sprites() :
                if sprite.z == layer :
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
    
