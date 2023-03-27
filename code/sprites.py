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
    def __init__(self, pos, surface, groups, z=cg.LAYERS['main']):
        super().__init__(pos = pos,
                         surface = surface,
                         groups = groups,
                         z = cg.LAYERS['constraints'])
        self.hitbox = self.rect.copy()

class Trashcan(Generic) :
    def __init__(self, pos, surface, groups, player_sprite, color, interact_sprites):
        super().__init__(pos, surface, groups, z = cg.LAYERS['trashcans'])
        
        self.player_sprite = player_sprite
        self.interact_sprites = interact_sprites

        self.pos = pos
        self.color = color
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)

        for button in self.interact_sprites :
            if button.pos == self.pos :
                self.button = button
                
        self.can_show_button = True
        self.hitbox = self.rect.copy()
        self.is_empty = False

    def update(self, dt) :
        self.is_colliding()

    def is_colliding(self) :
        for sprite in self.player_sprite.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_e] :
                        self.empty()
                        self.button.hide()

                    if self.can_show_button :
                        self.button.show()

                    self.can_show_button = False
                else :
                    if not self.can_show_button :
                        self.button.hide()

                    if not self.is_empty :
                        self.can_show_button = True

    def empty(self) :
        # update sprite and set is_empty to true
        if not self.is_empty :
            if self.color == 'green' :
                image_surface = pygame.image.load('./graphics/tiles/trashcans/green.png').convert_alpha()
            elif self.color == 'white' :
                image_surface = pygame.image.load('./graphics/tiles/trashcans/white.png').convert_alpha()
            elif self.color == 'blue' :
                image_surface = pygame.image.load('./graphics/tiles/trashcans/blue.png').convert_alpha()
            elif self.color == 'pink' :
                image_surface = pygame.image.load('./graphics/tiles/trashcans/pink.png').convert_alpha()

            self.image = image_surface
            self.is_empty = True
        
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