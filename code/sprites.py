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
        #self.hitbox.top -= 10

class Door(Generic) :
    def __init__(self, pos, frames, groups, offset):

        # animation setup
        self.frames = frames
        self.frame_index = 4

        # sprite setup
        super().__init__(pos = pos,
                         surface = self.frames[self.frame_index],
                         groups = groups,
                         z = cg.LAYERS['doors'])

        #self.hitbox = self.rect.copy().inflate(-40, 20)
        # offset door to be in middle of door frame
        self.offset_x(offset)

    def update(self, dt) :
        self.animate_close(dt)

    def offset_x(self, offset) :
        offset_x = self.rect.x - offset
        self.rect.topleft = (offset_x, self.rect.y)

    def set_open_animation(self, direction) :
        if direction == 'left' :
            self.frames = import_folder('./graphics/animated_tiles/left_door')
        else :
            self.frames = import_folder('./graphics/animated_tiles/right_door')

    def animate_open(self, dt) :
        if self.frame_index < (len(self.frames) / 2) - 1 :
            self.frame_index += cg.DOOR_ANIMATION_SPEED * dt
        else :
            self.frame_index = 4

        self.image = self.frames[int(self.frame_index)]

    def animate_close(self, dt) :
        if self.frame_index > 0 :
            self.frame_index -= cg.DOOR_ANIMATION_SPEED * dt
        else :
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]