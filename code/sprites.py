import pygame
import config as cg
from support import *

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
        self.frames[0] = pygame.image.load('./graphics/tiles/indicator/0.png').convert_alpha()
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
        self.image.set_alpha(255)

    def hide(self) :
        self.image.set_alpha(0)

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
                        print('calling interact')
                        self.interact()

                    if self.can_show_button and self.has_buttons :
                        self.button.show()

                    self.can_show_button = False
                else :
                    if not self.can_show_button and self.has_buttons :
                        self.button.hide()

                    if not self.interacted :
                        self.can_show_button = True

class Trashcan(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, z = cg.LAYERS['trashcans']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.color = self.button.name
        self.has_buttons = True
        self.interacted = False
        
        # collision
        self.hitbox = self.rect.copy()
    
    def interact(self) :
        self.empty()
    
    def empty(self) :
        # update sprite and set interacted to true
        if not self.interacted :
            image_surface = pygame.image.load(f'./graphics/tiles/trashcans/{self.color}.png').convert_alpha()

            self.image = image_surface
            self.interacted = True

class Toy(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, type, interact_sprites, player, z=cg.LAYERS['floor_decoration']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.type = type
        self.player = player
        self.interacted = False
        self.has_buttons = True

        # collision
        self.hitbox = self.rect.copy()

    def interact(self) :
        self.pickup()

    def pickup(self) :
        if not self.interacted and self.player.is_holding == 'None' :
            self.image.set_alpha(0)

            self.player.is_holding = self.type
            self.interacted = True

class Basket(InteractableObject) :
    def __init__(self, pos, name, surface, groups, player_sprite, interact_sprites, player, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)
        
        self.name = name
        self.player = player
        self.has_buttons = True
        self.interacted = False

        self.hitbox = self.rect.copy().inflate((-10, 0))
        self.hitbox.y -= 20

    def interact(self) :
        self.pickup()

    def pickup(self) :
        if not self.interacted and self.player.is_holding == 'None' :
            image_surface = pygame.image.load(f'./graphics/tiles/bathroom/basket.png').convert_alpha()
            self.image = image_surface

            self.player.is_holding = self.name
            self.interacted = True

class LaundryMachine(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, indicator_sprites, player, z = cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.has_buttons = False
        self.interacted = False
        self.running = False

        for sprite in indicator_sprites :
            if sprite.name == 'laundry' :
                self.indicator = sprite
        
        # collision
        self.player = player    
        self.hitbox = self.rect.copy().inflate((20, 20))
        self.hitbox.y += 35

    def update(self, dt) :
        if self.player.is_holding in ['basket_1', 'basket_2'] :
            self.indicator.show()
            self.indicator.animate(dt)
        else :
            self.indicator.hide()

    def interact(self) :
        print('colliding')
        self.put_away_laundry()

    def put_away_laundry(self) :
        if self.player.is_holding in ['basket_1', 'basket_2'] :
            self.player.is_holding = 'None'

class Dresser(InteractableObject) :
    def __init__(self, pos, surface, groups, player_sprite, interact_sprites, indicator_sprites, player, parts, z=cg.LAYERS['furniture']):
        super().__init__(pos, surface, groups, player_sprite, interact_sprites, z)

        # setup
        self.has_buttons = False
        self.interacted = False

        self.slots_filled = 0
        self.parts = parts

        for sprite in indicator_sprites :
            if sprite.name == 'dresser' :
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
                    # player coming from left
                    if not self.collision :
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