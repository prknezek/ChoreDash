import pygame
import config as cg
from support import *
from random import randint
from pygame import mixer

class Generic(pygame.sprite.Sprite) :
    def __init__(self, pos, surface, groups, z = cg.LAYERS['main']) :
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Constraint(Generic) :
    def __init__(self, pos, surface, groups, z = cg.LAYERS['constraints']):
        super().__init__(pos, surface, groups, z)
        self.hitbox = self.rect.copy()

class InteractButton(Generic) :
    def __init__(self, pos, name, surface, groups, z=cg.LAYERS['interact_buttons']):
        super().__init__(pos, surface, groups, z)

        self.pos = pos
        self.name = name
        self.image = pygame.image.load('./graphics/tiles/interact_buttons/e.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.hide()

    def show(self) :
        self.image.set_alpha(255)

    def hide(self) :
        self.image.set_alpha(0)

class Indicator(Generic) :
    def __init__(self, pos, name, frames, groups, player, z=cg.LAYERS['interact_buttons']):
        
        # setup
        self.name = name

        self.frames = frames
        self.frames_copy = frames
        self.frame_index = 0

        super().__init__(pos, self.frames[self.frame_index], groups, z)

        self.player = player
        self.hide()

    def animate(self, dt) :
        if self.frame_index < len(self.frames) - 1:
            self.frame_index += cg.INDICATOR_ANIMATION_SPEED * dt
        else :
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def show(self) :
        self.frames = self.frames_copy
        self.image = self.frames[int(self.frame_index)]

    def hide(self) :
        self.frames = pygame.image.load('./graphics/tiles/indicator/empty.png').convert_alpha()
        self.image = self.frames

class InteractableObject(Generic) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, z):
        super().__init__(pos, surface, groups, z)

        self.interact_sprites = interact_sprites
        self.pos = pos

        self.has_buttons = True
        self.can_show_button = True
        self.interacted = False

        for button in self.interact_sprites :
            if button.pos == self.pos :
                self.button = button
                
        # collision
        self.player_sprite = player_sprite

    def update(self, dt) :
        self.is_colliding()

    def interact(self) :
        pass

    # calls self.interact() if player is colliding with object
    def is_colliding(self) :
        for sprite in self.player_sprite.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :                    
                    keys = pygame.key.get_pressed()

                    if self.has_buttons :
                        if keys[pygame.K_e] :
                            self.interact()
                            self.button.hide()
                    else :
                        self.interact()

                    if self.can_show_button and self.has_buttons :
                        self.button.show()

                    self.can_show_button = False
                else :                    
                    if not self.can_show_button and self.has_buttons :
                        self.button.hide()

                    if not self.interacted :
                        self.can_show_button = True

class BarBG(Generic) :
    def __init__(self, pos, surface, groups, z=cg.LAYERS['decoration']):
        super().__init__(pos, surface, groups, z)

    def show(self):
        self.image.set_alpha(255)
    
    def hide(self) :
        self.image.set_alpha(0)

class SpamBar(Generic) :
    def __init__(self, pos, surface, groups, bg, z=cg.LAYERS['trashcans']):
        super().__init__(pos, surface, groups, z)

        self.rect = self.image.get_rect(topleft = pos)
        self.bg = bg

        self.pos = pos
        self.finished = False

        self.max_presses = 200
        self.press_amount = 0

        self.bg.hide()

    def update(self, dt) :
        #self.image = pygame.transform.scale(self.image, (10, 12))
        self.update_bar()
        pass

    def update_bar(self) :
        if not self.finished :
            width = (self.press_amount / self.max_presses * 23) + 1
            self.image = pygame.transform.scale(self.image, (width, 6))
            self.rect = self.image.get_rect(topleft = self.pos)

    def do_work(self) :
        # spamming e
        self.press_amount += 1
        if self.press_amount >= self.max_presses :
            self.finished = True

class Toilet(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, progress_bar, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.hitbox = self.rect.copy()
        self.hitbox.y -= 20

        self.button.rect.y += 32
        self.bar = progress_bar
        self.showing_bar = False

        self.is_clean = False
        self.bar.image.set_alpha(0)

    def update(self, dt) :
        self.is_colliding()
        if self.bar.finished :
            self.interacted = True
            self.button.hide()
            self.is_clean = True
            self.bar.bg.kill()
            self.bar.kill()
            self.image = pygame.image.load('./graphics/tiles/bathroom/clean_toilet.png').convert_alpha()

    def interact(self) :
        self.bar.do_work()

    def is_colliding(self) :
        for sprite in self.player_sprite.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :                    
                    keys = pygame.key.get_pressed()

                    if self.has_buttons :
                        if keys[pygame.K_e] :
                            self.bar.image.set_alpha(255)
                            self.bar.bg.show()
                            self.interact()
                    else :
                        self.interact()

                    if self.can_show_button and self.has_buttons :
                        self.button.show()

                    self.can_show_button = False
                else :                    
                    if not self.can_show_button and self.has_buttons :
                        self.button.hide()

                    if not self.interacted :
                        self.can_show_button = True


class Trash(InteractableObject) :
    def __init__(self, pos, surface, groups, player, player_sprite, interact_sprites, has_buttons, z = cg.LAYERS['decoration']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.has_buttons = has_buttons
        self.can_show_button = has_buttons

        self.hitbox = self.rect.copy().inflate(-12, -12)
        self.player = player
        self.hitbox.y -= 14

    def interact(self) :
        if self.player.has_broom and not self.has_buttons:
            self.kill()
        elif self.has_buttons :
            self.button.kill()
            self.kill()

class Fridge(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.show_todolist = False
        self.has_buttons = False

        self.hitbox = self.rect.copy()
        self.hitbox.y -= 20

    def update(self, dt) :
        self.is_colliding() 
        if not self.can_show_button :
            self.show_todolist = True
        else :
            self.show_todolist = False
        
class Dishes(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, player, z = cg.LAYERS['decoration']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.hitbox = self.rect.copy()
        self.hitbox.y += 10
        self.is_washing = False
        self.clean = False
        self.updated_image = False
        self.put_away = False
        self.player = player
        self.display_message = 'None' 
    
    def interact(self) :
        self.display_message = 'None' 
        if not self.clean:
            if self.player.is_holding == 'None' :
                self.is_washing = True
            else :
                self.display_message = 'cannot perform while holding item'
        else :
            if self.player.is_holding == 'None' :
                self.interacted = True
                self.put_away = True
                self.image.set_alpha(0)
            else :
                self.display_message = 'cannot perform while holding item'

    def update(self, dt) :
        self.is_colliding()
        if self.clean and not self.updated_image :
            self.updated_image = True
            self.image = pygame.image.load('./graphics/tiles/clean_minigame/clean_dishes.png').convert_alpha()

class Trashcan(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, z = cg.LAYERS['trashcans']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.color = self.button.name
        self.has_buttons = True

        # game
        self.letter_sequence = []
        self.step = 0
        self.do_sequence = False
        self.moved_letter = False
        
        # collision
        self.hitbox = self.rect.copy()

    def update(self, dt) :
        self.is_colliding()
        if self.do_sequence :
            self.run_sequence()

    def interact(self) :
        if not self.do_sequence :
            self.start_sequence()
    
    def start_sequence(self) :
        sequence_length = randint(3, 5)

        for i in range(sequence_length) :
            key = randint(1, 24)
            key += 96 # convert to ascii
            while key in [117, 118, 119, 97, 115, 100, 101] :
                key = randint(1, 24)
                key += 96
            self.letter_sequence.append(key)

        self.do_sequence = True
    
    def run_sequence(self) :
        if self.step == len(self.letter_sequence) :
            self.do_sequence = False
            self.interacted = True
            self.empty()

        if not self.interacted :
            keys = pygame.key.get_pressed()
            letter = chr(self.letter_sequence[self.step])

            self.move_letter()

            self.button.image = pygame.image.load(f'./graphics/tiles/alphabet/{letter}.png').convert_alpha()
            if (keys[self.letter_sequence[self.step]]) :
                self.step += 1

    def move_letter(self) :
        if not self.moved_letter :
            self.button.rect.x += 8
            self.button.rect.y += 4
            self.moved_letter = True

    def empty(self) :
        # update sprite and set interacted to true
        image_surface = pygame.image.load(f'./graphics/tiles/trashcans/{self.color}.png').convert_alpha()
        self.image = image_surface
        self.button.hide()

    def is_colliding(self) :
        for sprite in self.player_sprite.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :                    
                    keys = pygame.key.get_pressed()

                    if self.has_buttons :
                        if keys[pygame.K_e] :
                            self.interact()
                    else :
                        self.interact()

                    if self.can_show_button and self.has_buttons :
                        self.button.show()

                    self.can_show_button = False
                else :                    
                    if not self.can_show_button and self.has_buttons :
                        self.button.hide()

                    if not self.interacted :
                        self.can_show_button = True

class Basket(InteractableObject) :
    def __init__(self, pos, name, surface, groups, player_sprite, interact_sprites, laundry_machine, player, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)
        
        self.name = name
        self.player = player
        self.laundry_machine = laundry_machine
        self.display_message = 'None' 

        self.hitbox = self.rect.copy().inflate((-10, 0))
        self.hitbox.y -= 20

    def interact(self) :
        self.pickup()

    def pickup(self) :
        # pickup laundry
        if self.laundry_machine.contains == 'None' :
            if not self.interacted :
                if self.player.is_holding == 'None' :
                    image_surface = pygame.image.load('./graphics/tiles/bathroom/basket.png').convert_alpha()
                    self.image = image_surface

                    self.player.is_holding = self.name
                    self.interacted = True
                    self.display_message = 'None'
                else :
                    self.display_message = 'cannot perform while holding item'
        else :
            self.display_message = 'Cannot perform while laundry full'

class LaundryMachine(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, indicator_sprites, player, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.has_buttons = False
        self.contains = 'None'
        self.show_indicator = False
        self.clean = False
        self.display_message = 'None' 

        # animation
        self.frames = import_folder('./graphics/animated_tiles/laundry_machine')
        self.frame_index = 0

        # timer setup
        self.start_cycle = False
        self.last_time = 0
        self.seconds = cg.LAUNDRY_CYCLE_LENGTH

        for sprite in indicator_sprites :
            if 'laundry' in sprite.name :
                self.indicator = sprite
        
        self.button.rect.x += 16
        #self.button.rect.y += 16

        # collision
        self.player = player    
        self.hitbox = self.rect.copy()
        self.hitbox.y -= 20

        #sounds
        # self.washsfx = mixer.Sound('./audio/wash_mac.mp3')
        # self.ping = mixer.Sound('./audio/ping.mp3')

    def update(self, dt) :
        self.tick_timer()
        self.is_colliding()

        if self.player.is_holding in ['basket_1', 'basket_2'] :
            self.show_indicator = True

        self.indicator_control(dt)

        if self.start_cycle :
            # self.washsfx.set_volume(0.1)
            # self.washsfx.play()
            self.animate(dt)

        if self.clean :
            self.image = pygame.image.load('./graphics/tiles/bathroom/laundry_machine_done.png').convert_alpha()
            # self.washsfx.stop()
            
        elif not self.start_cycle :
            self.image = pygame.image.load('./graphics/tiles/bathroom/laundry_machine.png').convert_alpha()



    def animate(self, dt) :
        if self.frame_index < len(self.frames) - 1 :
            self.frame_index += cg.LAUNDRY_ANIMATION_SPEED * dt
        else :
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def interact(self) :
        # get laundry out of machine
        if self.has_buttons :
            self.get_laundry()
        # place laundry in machine
        if not self.start_cycle and not self.has_buttons :
            self.put_away_laundry()

    def put_away_laundry(self) :
        if self.player.is_holding in ['basket_1', 'basket_2'] and self.contains == 'None' :
            self.contains = self.player.is_holding
            self.player.is_holding = 'None'
            self.show_indicator = False
            self.start_cycle = True

    def get_laundry(self) :
        if self.player.is_holding == 'None' :
            self.has_buttons = False
            self.show_indicator = False
            self.display_message = 'None' 
            self.clean = False
            self.player.is_holding = self.contains
            self.contains = 'None'
        else :
            self.display_message = 'Cannot perform while holding item' 

    def tick_timer(self) :
        if not self.start_cycle :
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000 :
            self.last_time = current_time
            self.seconds -= 1
            if self.seconds == 0 :
                self.show_indicator = True
                self.has_buttons = True
                self.start_cycle = False
                self.clean = True

                self.last_time = 0
                self.seconds = cg.LAUNDRY_CYCLE_LENGTH
                self.contains = self.contains + '_clean'
    
    def indicator_control(self, dt) :
        if self.show_indicator :
            self.indicator.show()
            self.indicator.animate(dt)
        else :
            self.indicator.hide()
        
class TowelRack(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, indicator_sprites, player, z = cg.LAYERS['wall_decoration']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.has_buttons = False
        self.is_empty = True
        self.indicators = []

        for sprite in indicator_sprites :
            if 'towel' in sprite.name :
                self.indicators.append(sprite)

        self.player = player
        self.hitbox = self.rect.copy()
    
    def update(self, dt) :
        self.is_colliding()

        if self.player.is_holding == 'basket_2_clean' and self.is_empty :
            self.has_buttons = True
            for indicator in self.indicators :
                indicator.show()
                indicator.animate(dt)
        else :
            self.has_buttons = False
            for indicator in self.indicators :
                indicator.hide()

    def interact(self) :
        self.place_towel()

    def place_towel(self) :
        if self.is_empty :
            if self.player.is_holding == 'basket_2_clean' :
                self.image = pygame.image.load('./graphics/tiles/bathroom/towel_rack_full.png').convert_alpha()
                self.is_empty = False
                self.player.is_holding = 'None'
                self.interacted = True

class BedSheet(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, indicator_sprites, player, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.has_buttons = False
        self.is_made = False
        self.indicators = []

        self.button.rect.x += 16
        self.button.rect.y += 16

        for sprite in indicator_sprites :
            if 'bed' in sprite.name :
                self.indicators.append(sprite)

        self.player = player
        self.hitbox = self.rect.copy()
        self.image = pygame.image.load('./graphics/tiles/bathroom/bedsheet.png').convert_alpha()
        self.image.set_alpha(0)

    def update(self, dt) :
        self.is_colliding()

        if self.player.is_holding == 'basket_1_clean' and not self.is_made :
            self.has_buttons = True
            for indicator in self.indicators :
                indicator.show()
                indicator.animate(dt)
        else :
            self.has_buttons = False
            for indicator in self.indicators :
                indicator.hide()

    def interact(self) :
        self.make_bed()

    def make_bed(self) :
        if not self.is_made :
            if self.player.is_holding == 'basket_1_clean' :
                self.image.set_alpha(255)
                self.player.is_holding = 'None'
                self.interacted = True
                self.is_made = True

class Toy(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, type, interact_sprites, player, z=cg.LAYERS['floor_decoration']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.type = type
        self.player = player

        # collision
        self.hitbox = self.rect.copy()

    def interact(self) :
        self.pickup()

    def pickup(self) :
        if not self.interacted and self.player.is_holding == 'None' :
            self.image.set_alpha(0)

            self.player.is_holding = self.type
            self.interacted = True

class Dresser(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, indicator_sprites, player, parts, z=cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.has_buttons = False

        self.slots_filled = 0
        self.parts = parts

        for sprite in indicator_sprites :
            if 'dresser' in sprite.name :
                self.indicator = sprite

        # rearrange order
        self.parts.reverse()
        parts.insert(1, self)

        temp = self.parts[3]
        self.parts[3] = self.parts[2]
        self.parts[2] = temp

        # collision
        self.player = player
        self.hitbox = self.rect.copy().inflate((20, 0))
        self.hitbox.x += 20
        self.hitbox.y -= 20

    def update(self, dt) :
        self.is_colliding()
        if self.player.is_holding in ['bear', 'basket_ball', 'car', 'dumbbell'] :
            self.indicator.show()
            self.indicator.animate(dt)
        else :
            self.indicator.hide()

    def interact(self) :
        self.put_away_toy()

    def put_away_toy(self) :
        if self.slots_filled < 4 :
            if self.player.is_holding in ['bear', 'basket_ball', 'car', 'dumbbell'] :
                self.player.is_holding = 'None'
                self.parts[self.slots_filled].image = pygame.image.load(f'./graphics/tiles/dresser/{self.slots_filled}.png').convert_alpha()
                
                self.slots_filled += 1

class Door(Generic) :
    def __init__(self, pos, frames, groups, offset, player_sprite):
        # collision
        self.player_sprite = player_sprite

        # animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(pos = pos,
                         surface = self.frames[self.frame_index],
                         groups = groups,
                         z = cg.LAYERS['doors'])

        # offset door to be in middle of door frame
        self.hitbox = self.rect.copy().inflate(-30, 0)
        self.hitbox.x -= 10
        self.offset_x(offset)
        self.do_animation = False
        self.collision = False
        self.original_rect_x = self.rect.x

    def update(self, dt) :
        self.is_colliding()
        if self.do_animation :
            self.animate_open(dt)
        else :
            self.animate_close(dt)

    def is_colliding(self) :
        for sprite in self.player_sprite.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :
                    if not self.collision :
                        # player coming from left
                        if sprite.direction.x > 0 :
                            self.set_open_animation('right')
                            if self.rect.x != self.original_rect_x :
                                self.rect.x = self.original_rect_x
                        # player coming from right
                        if sprite.direction.x < 0 :
                            self.set_open_animation('left')
                            if self.rect.x == self.original_rect_x:
                                self.offset_x(20)
                        
                    self.do_animation = True
                    self.collision = True
                else :
                    self.collision = False


    def offset_x(self, offset) :
        rect_offset_x = self.rect.x - offset
        self.rect.topleft = (rect_offset_x, self.rect.y)

    def set_open_animation(self, direction) :
        if direction == 'left' :
            self.frames = import_folder('./graphics/animated_tiles/left_door')
        else :
            self.frames = import_folder('./graphics/animated_tiles/right_door')

    def animate_open(self, dt) :
        if self.frame_index < len(self.frames) - 1 :
            self.frame_index += cg.DOOR_ANIMATION_SPEED * dt
        else :
            self.frame_index = 4
        if self.frame_index == 4 :
            self.do_animation = False

        self.image = self.frames[int(self.frame_index)]

    def animate_close(self, dt) :
        if self.frame_index > 0 :
            self.frame_index -= cg.DOOR_ANIMATION_SPEED * dt
        else :
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

class DustParticle(Generic) :
    def __init__(self, pos, groups, player, z=cg.LAYERS['floor_decoration']):

        self.player = player
        self.pos = pos

        # animation
        self.set_dust_run_particles('horizontal')
        self.frame_index = 0

        super().__init__(pos, self.frames[self.frame_index], groups, z)

    def update(self, dt) :
        self.animate_dust(dt)

    def set_dust_run_particles(self, direction) :
        if direction == 'horizontal' :
            self.frames = import_folder('./graphics/character/dust_particles/horizontal/')
        else :
            self.frames = import_folder('./graphics/character/dust_particles/vertical/')

    def animate_dust(self, dt) :
        if 'idle' not in self.player.status : # player is moving
            self.image.set_alpha(255)
            if self.player.status in ['right', 'left'] :
                self.set_dust_run_particles('horizontal')
            else :
                self.set_dust_run_particles('vertical')
    
            self.frame_index += cg.DUST_ANIMATION_SPEED * dt
            if self.frame_index >= len(self.frames) :
                self.frame_index = 0

            if self.player.status == 'right' :
                self.pos = self.player.pos + pygame.math.Vector2(-24, 28)
                self.rect.bottomleft = self.pos

                dust_particle = self.frames[int(self.frame_index)]
                self.image = dust_particle
            elif self.player.status == 'left' :
                self.pos = self.player.pos + pygame.math.Vector2(8, 28)
                self.rect.bottomleft = self.pos

                dust_particle = self.frames[int(self.frame_index)]
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.image = flipped_dust_particle
            elif self.player.status == 'down' :
                self.pos = self.player.pos
                self.rect.bottomleft = self.pos + pygame.math.Vector2(-8, -6)

                dust_particle = self.frames[int(self.frame_index)]
                flipped_dust_particle = pygame.transform.flip(dust_particle, False, True)
                self.image = flipped_dust_particle
            elif self.player.status == 'up' :
                self.pos = self.player.pos
                self.rect.bottomleft = self.pos + pygame.math.Vector2(-8, 40)

                dust_particle = self.frames[int(self.frame_index)]
                self.image = dust_particle
        else :
            self.frame_index = 0
            self.image.set_alpha(0)

class Broom(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, trash_sprites, player, z = cg.LAYERS['decoration']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        self.player = player
        self.display_message = 'None'
        self.hitbox = self.rect.copy().inflate((-10, -20))
        self.trash_sprites = trash_sprites
    
    def interact(self) :
        self.player.has_broom = True
        self.interacted = True
        self.image.set_alpha(0)