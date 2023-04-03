import pygame
import config as cg
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *
from todolist import TaskIndex
from camera_group import CameraGroup
from clean_minigame import CleanMinigame

class Level :
    def __init__(self) :
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # task completion trackers
        self.completed_array = [False, False, False, False, False, False, False]

        # sprite groups
        self.all_sprites = CameraGroup()

        self.collision_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.trashcan_sprites = pygame.sprite.Group()
        self.interact_sprites = pygame.sprite.Group()
        self.indicator_sprites = pygame.sprite.Group()
        self.floor_trash_sprites = pygame.sprite.Group()
        self.counter_trash_sprites = pygame.sprite.Group()

        # fonts
        self.equip_font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.equip_bgfont = pygame.font.Font('graphics/5x5.ttf', 15)
        self.warning_font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.warning_bgfont = pygame.font.Font('graphics/5x5.ttf', 15)
        self.warning_items = []

        # text timer setup
        self.last_time = 0
        self.seconds = 3
        self.countdown = False

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
        self.clean_minigame = CleanMinigame(self.player, self.player_sprite, self.collision_sprites)

        # create dust particle object
        DustParticle(self.player.pos, self.all_sprites, self.player)

        # draw fridge
        for obj in tmx_data.get_layer_by_name('Fridge') :
            self.fridge = Fridge((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites)

        # draw interact buttons
        for obj in tmx_data.get_layer_by_name('InteractButtons') :
            InteractButton((int(obj.x), int(obj.y)), obj.name, self.display_surface, [self.all_sprites, self.interact_sprites])
        
        # draw indicator tiles
        
        for obj in tmx_data.get_layer_by_name('Indicators') :
            if 'vertical' in obj.name :
                indicator_frames = import_folder('./graphics/tiles/indicator/vertical')
            else :
                indicator_frames = import_folder('./graphics/tiles/indicator/horizontal')

            if 'floor' in obj.name :
                z = cg.LAYERS['floor_decoration']
            else :
                z = cg.LAYERS['interact_buttons']
            
            Indicator((int(obj.x), int(obj.y)), obj.name, indicator_frames, [self.all_sprites, self.indicator_sprites], self.player, z)

        # draw dishes
        for obj in tmx_data.get_layer_by_name('Dishes') :
            self.dishes = Dishes((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.player)
            self.warning_items.append(self.dishes)

        # draw laundry machine
        for obj in tmx_data.get_layer_by_name('Laundry') :
            if obj.name == 'laundry_machine' :
                self.laundry_machine = LaundryMachine((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player)
                self.warning_items.append(self.laundry_machine)

        # draw laundry baskets
        self.baskets = []
        for obj in tmx_data.get_layer_by_name('Laundry') :
            if 'basket' in obj.name :
                self.baskets.append(Basket((int(obj.x), int(obj.y)), obj.name, obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.laundry_machine, self.player))
        
        self.warning_items.append(self.baskets[0])
        self.warning_items.append(self.baskets[1])

        # draw bed
        for obj in tmx_data.get_layer_by_name('BedSheet') :
            self.bed = BedSheet((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player)

        # draw towel rack
        for obj in tmx_data.get_layer_by_name('TowelRack') :
            self.towel_rack = TowelRack((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player)

        # draw toys
        for obj in tmx_data.get_layer_by_name('Toys') :
            self.toy = Toy((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, obj.name, self.interact_sprites, self.player)

        # draw dresser
        parts = self.draw_generic_tiles('Dresser', 'furniture')
        for x, y, surface in tmx_data.get_layer_by_name('Dresser').tiles() :
            if (x, y) == (19, 18) :
                self.dresser = Dresser((x * cg.TILESIZE, y * cg.TILESIZE), surface, self.all_sprites, self.player_sprite, self.interact_sprites, self.indicator_sprites, self.player, parts)                

        # draw trashcans
        for x, y, surface in tmx_data.get_layer_by_name('Trashcans').tiles() :
            Trashcan((x * cg.TILESIZE, y * cg.TILESIZE), surface, [self.all_sprites, self.trashcan_sprites], self.player_sprite, self.interact_sprites)
        
        # draw trash
        for x, y, surface in tmx_data.get_layer_by_name('Trash').tiles() :
            Trash((x * cg.TILESIZE, y * cg.TILESIZE), surface, [self.all_sprites, self.floor_trash_sprites], self.player, self.player_sprite, self.interact_sprites, False)

        for x, y, surface in tmx_data.get_layer_by_name('CounterTrash').tiles() :
            Trash((x * cg.TILESIZE, y * cg.TILESIZE), surface, [self.all_sprites, self.counter_trash_sprites], self.player, self.player_sprite, self.interact_sprites, True, z = cg.LAYERS['in_front_decoration'])

        # draw broom
        for obj in tmx_data.get_layer_by_name('Broom') :
            broom = Broom((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, self.floor_trash_sprites, self.player)
            self.warning_items.append(broom)
        
        # draw progress bar
        bar_bg = pygame.image.load('./graphics/tiles/indicator/bar_bg.png').convert_alpha()
        bg = BarBG((992, 586), bar_bg, self.all_sprites)
        image = pygame.image.load('./graphics/tiles/indicator/bar.png').convert_alpha()
        progress_bar = SpamBar((996, 599), image, self.all_sprites, bg)

        # draw toilet
        for obj in tmx_data.get_layer_by_name('Toilet') :
            self.toilet = Toilet((int(obj.x), int(obj.y)), obj.image, self.all_sprites, self.player_sprite, self.interact_sprites, progress_bar)

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
            
            # equip message
            text_surf = self.equip_bgfont.render(item + " EQUIPPED", False, 'Black')
            text_surf_rect = text_surf.get_rect(center = (cg.SCREEN_WIDTH/2 + 1, cg.SCREEN_HEIGHT - 20 + 2))
            self.display_surface.blit(text_surf, text_surf_rect)
            text_surf = self.equip_font.render(item + " EQUIPPED", False, 'White')
            text_surf_rect = text_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT - 20))
            self.display_surface.blit(text_surf, text_surf_rect)
        # warning messages
        for item in self.warning_items :
            if item.display_message != 'None' :
                text_surf = self.warning_bgfont.render(f"{item.display_message}", False, 'Black')
                text_surf_rect = text_surf.get_rect(center = (cg.SCREEN_WIDTH/2 + 1, cg.SCREEN_HEIGHT - 40 + 2))
                self.display_surface.blit(text_surf, text_surf_rect)
                text_surf = self.warning_font.render(f"{item.display_message}", False, 'White')
                text_surf_rect = text_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT - 40))
                self.display_surface.blit(text_surf, text_surf_rect)

                self.countdown = True
                self.text_timer()

    def text_timer(self) :
        if not self.countdown :
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000 :
            self.last_time = current_time
            self.seconds -= 1
            if self.seconds == 0 :
                for item in self.warning_items :
                    item.display_message = 'None'

                self.countdown = False
                self.seconds = 3
                self.last_time = 0

    def event_detection(self, dt) :
        empty_count = 0

        # dishes minigame
        if self.dishes.is_washing :
            self.clean_minigame.run(dt)

            if self.clean_minigame.won :
                self.dishes.is_washing = False
                self.dishes.clean = True
            elif self.clean_minigame.loss :
                self.dishes.is_washing = False
                self.clean_minigame = CleanMinigame(self.player, self.player_sprite, self.collision_sprites)
                self.player.lives = 3
            
        if self.toilet.is_clean :
            self.completed_array[TaskIndex.TOILET.value] = True
        
        if self.dishes.put_away :
            self.completed_array[TaskIndex.DISHES.value] = True

        if len(self.floor_trash_sprites.sprites()) == 0 :
            self.completed_array[TaskIndex.CLEAN_FLOORS.value] = True
        
        if len(self.counter_trash_sprites.sprites()) == 0 :
            self.completed_array[TaskIndex.CLEAR_COUNTER.value] = True

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
                if (x, y) != (19, 18) :
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