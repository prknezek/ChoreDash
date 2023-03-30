import pygame
import config as cg
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *
from todolist import TaskIndex
from random import randint, uniform

class Level :
    def __init__(self) :
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # task completion trackers
        self.completed_array = [False, False, False, False]

        # sprite groups
        self.all_sprites = CameraGroup()

        self.collision_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.trashcan_sprites = pygame.sprite.Group()
        self.interact_sprites = pygame.sprite.Group()
        self.indicator_sprites = pygame.sprite.Group()

        self.font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.bgfont = pygame.font.Font('graphics/5x5.ttf', 15)

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

        # draw player
        for obj in tmx_data.get_layer_by_name('Player') :
            if obj.name == 'Start' :
                self.player = Player((obj.x, obj.y), [self.all_sprites, self.player_sprite], self.collision_sprites, self.door_sprites)

        # create clean minigame
        self.clean_minigame = CleanMinigame(self.player, self.player_sprite)

        # draw fridge
        for obj in tmx_data.get_layer_by_name('Fridge') :
            self.fridge = Fridge((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites)

        # draw interact buttons
        for obj in tmx_data.get_layer_by_name('InteractButtons') :
            InteractButton((int(obj.x), int(obj.y)), obj.name, self.display_surface, [self.all_sprites, self.interact_sprites])
        
        # draw indicator tiles
        indicator_frames = import_folder('./graphics/tiles/indicator')
        for obj in tmx_data.get_layer_by_name('Indicators') :
            Indicator((int(obj.x), int(obj.y)), obj.name, indicator_frames, [self.all_sprites, self.indicator_sprites], self.player)

        # draw dishes
        for obj in tmx_data.get_layer_by_name('Dishes') :
            self.dishes = Dishes((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites)

        # draw laundry machine
        for obj in tmx_data.get_layer_by_name('Laundry') :
            if obj.name == 'laundry_machine' :
                laundry_machine = LaundryMachine((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player)

        # draw laundry baskets
        for obj in tmx_data.get_layer_by_name('Laundry') :
            if 'basket' in obj.name :
                Basket((int(obj.x), int(obj.y)), obj.name, obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, laundry_machine, self.player)
        
        # draw bed
        for obj in tmx_data.get_layer_by_name('BedSheet') :
            self.bed = BedSheet((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player)

        # draw towel rack
        for obj in tmx_data.get_layer_by_name('TowelRack') :
            self.towel_rack = TowelRack((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player)

        # draw toys
        for obj in tmx_data.get_layer_by_name('Toys') :
            Toy((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, obj.name, self.interact_sprites, self.player)

        # draw dresser
        parts = self.draw_generic_tiles('Dresser', 'furniture')
        for x, y, surface in tmx_data.get_layer_by_name('Dresser').tiles() :
            if (x, y) == (19, 14) :
                self.dresser = Dresser((x * cg.TILESIZE, y * cg.TILESIZE), surface, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player, parts)                

        # draw trashcans
        for x, y, surface in tmx_data.get_layer_by_name('Trashcans').tiles() :
            Trashcan((x * cg.TILESIZE, y * cg.TILESIZE), surface, [self.all_sprites, self.trashcan_sprites], self.player_sprite, self.interact_sprites)
        
        # draw door tiles
        door_frames = import_folder('./graphics/animated_tiles/right_door')

        for x, y, surface in tmx_data.get_layer_by_name('Doors').tiles() :
            Door(pos = (x * cg.TILESIZE, y * cg.TILESIZE),
                 frames = door_frames,
                 groups = [self.all_sprites, self.collision_sprites, self.door_sprites],
                 offset = cg.DOOR_TILE_OFFSET,
                 player_sprite = self.player_sprite)

        
    def run(self, dt, whether_to_update) :
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        if whether_to_update:
            self.all_sprites.update(dt)
        self.equip_message()
        self.event_detection(dt)

    def equip_message(self):
        item = "None"
        if self.player.is_holding != "None":
            if self.player.is_holding in ['basket_1_clean', 'basket_2_clean'] :
                item = "CLEAN LAUNDRY"
            elif self.player.is_holding in ['basket_1', 'basket_2'] :
                item = "LAUNDRY"
            elif self.player.is_holding == 'basket_ball' :
                item = "BASKETBALL"
            else :
                item = self.player.is_holding
            
            # testing equip message
            testing_surf = self.bgfont.render(item + " EQUIPPED", False, 'Black')
            testing_surf_rect = testing_surf.get_rect(center = (cg.SCREEN_WIDTH/2 + 1, cg.SCREEN_HEIGHT - 20 + 2))
            self.display_surface.blit(testing_surf, testing_surf_rect)
            testing_surf = self.font.render(item + " EQUIPPED", False, 'White')
            testing_surf_rect = testing_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT - 20))
            self.display_surface.blit(testing_surf, testing_surf_rect)

    def event_detection(self, dt) :
        empty_count = 0

        # dishes minigame
        if self.dishes.is_washing :
            self.clean_minigame.run(dt)

        for sprite in self.trashcan_sprites :
            if sprite.interacted :
                empty_count += 1
        
        if self.dresser.slots_filled == 4 :
            self.completed_array[TaskIndex.TOYS.value] = True

        if empty_count == 4 :
            self.completed_array[TaskIndex.TRASH.value] = True
        
        if self.bed.is_made and not self.towel_rack.is_empty :
            self.completed_array[TaskIndex.LAUNDRY.value] = True

    def draw_generic_tiles(self, tiled_name, layer_name) :
        tmx_data = load_pygame('./house/house_data/house.tmx')
        parts = []
        for x, y, surface in tmx_data.get_layer_by_name(tiled_name).tiles() :
            if tiled_name == 'Constraints' :
                Constraint((x * cg.TILESIZE, y * cg.TILESIZE), pygame.Surface((cg.TILESIZE, cg.TILESIZE)), self.collision_sprites)
            elif tiled_name == 'Dresser' :
                if (x, y) != (19, 14) :
                    tile = Generic((x * cg.TILESIZE, y * cg.TILESIZE), surface, self.all_sprites, cg.LAYERS[layer_name])
                    parts.append(tile)
            else :
                Generic((x * cg.TILESIZE, y * cg.TILESIZE), surface, self.all_sprites, cg.LAYERS[layer_name])
        
        return parts
                    
    
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

class CleanMinigame :
    def __init__(self, player, player_sprite) :
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        # spawning
        self.player_sprite = player_sprite
        self.player = player
        self.can_spawn_enemies = True
        self.enemy_spawn_pos = pygame.math.Vector2()
    
        # delay timing
        self.run_delay = False
        self.last_time = 0
        self.seconds = cg.ENEMY_SPAWN_INTERVAL

        # teleport
        self.teleport_to_start = False

    # constantly running
    def run(self, dt) :
        if not self.teleport_to_start :
            self.teleport_to_start = True
            self.player.pos.x += 200

        self.update_spawn_boundaries()
        self.enemy_spawn_delay()
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.player)

        if self.can_spawn_enemies :
            self.spawn_enemies()

    def spawn_enemies(self) :
        self.determine_spawn_location()

        Enemy(pos = (self.enemy_spawn_pos.x, self.enemy_spawn_pos.y), 
              group = self.all_sprites, 
              player_sprite = self.player_sprite,
              player = self.player)
        
        self.can_spawn_enemies = False
        self.run_delay = True

    def determine_spawn_location(self) :
        spawn_side = randint(1, 4)

        match spawn_side :
            case 1 : # top
                self.enemy_spawn_pos.y = randint(self.max_top_y, self.min_top_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.max_right_x)
            case 2 : # bottom
                self.enemy_spawn_pos.y = randint(self.min_bottom_y, self.max_bottom_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.max_right_x)
            case 3 : # left
                self.enemy_spawn_pos.y = randint(self.max_top_y, self.max_bottom_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.min_left_x)
            case 4 : # right
                self.enemy_spawn_pos.y = randint(self.max_top_y, self.max_bottom_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.max_right_x)

        print('enemy pos:')
        print(self.enemy_spawn_pos.x, self.enemy_spawn_pos.y)
        
    def update_spawn_boundaries(self) :
        pos_x = int(self.player.pos.x)
        pos_y = int(self.player.pos.y)

        max_spawn_distance = 250
        min_spawn_distance = 200

        self.max_right_x = pos_x + max_spawn_distance
        self.min_right_x = pos_x + min_spawn_distance
        self.max_left_x = pos_x - max_spawn_distance
        self.min_left_x = pos_x - min_spawn_distance

        self.max_bottom_y = pos_y + max_spawn_distance
        self.min_bottom_y = pos_y + min_spawn_distance
        self.max_top_y = pos_y - max_spawn_distance
        self.min_top_y = pos_y - min_spawn_distance

    def enemy_spawn_delay(self) :
        if not self.run_delay :
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000 :
            self.last_time = current_time
            self.seconds -= 1
            if self.seconds == 0 :
                self.can_spawn_enemies = True
                self.last_time = 0
                self.seconds = cg.ENEMY_SPAWN_INTERVAL

class Enemy(pygame.sprite.Sprite) :
    def __init__(self, pos, group, player_sprite, player) :
        super().__init__(group)

        # setup
        image_path = './graphics/tiles/clean_minigame/enemies/' + str(randint(1, 7)) + '.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.z = cg.LAYERS['main']

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = uniform(cg.ENEMY_MIN_SPEED, cg.ENEMY_MAX_SPEED)

        # collision
        self.hitbox = self.rect.copy().inflate((0, 0))
        self.player = player
        self.player_sprite = player_sprite

    def update(self, dt) :
        self.player_collision()
        self.move(dt)

    def player_collision(self) :
        player = self.player_sprite.sprites()[0]
        if player.hitbox.colliderect(self.hitbox) :
            # handle collision
            print('collided with player')

    def move(self, dt) :
        if self.pos != self.player.pos :
            if self.direction.magnitude() > 0 :
                self.direction = self.direction.normalize()
                
            stepx = self.player.pos.x - self.pos.x
            stepy = self.player.pos.y - self.pos.y

            # horizontal movement
            self.pos.x += stepx * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx

            # vertical movement
            self.pos.y += stepy * self.speed  * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery

            print(self.pos)