import pygame
import config as cg
from support import import_folder

class Tile(pygame.sprite.Sprite) :
    def __init__(self, size, x, y) :
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

    def update(self, horizontal_shift, vertical_shift) :
        self.rect.x += horizontal_shift
        self.rect.y += vertical_shift

class StaticTile(Tile) :
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class AnimatedTile(Tile) :
    # path is folder to multiple images (spritesheet)
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

class DoorTile(AnimatedTile) :
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        # offset door to be in the middle of the entrance
        self.offset_x(offset)

    def set_open_animation(self, path) :
        self.frames = import_folder(path)

    def offset_x(self, offset) :
        offset_x = self.rect.x - offset
        self.rect.topleft = (offset_x, self.rect.y)

    def animate_open(self) :
        if self.frame_index < (len(self.frames) / 2) - 1 :
            self.frame_index += cg.DOOR_ANIMATION_TIME
        else :
            self.frame_index = 4

        self.image = self.frames[int(self.frame_index)]
    
    def animate_close(self) :
        if self.frame_index > 0 :
            self.frame_index -= cg.DOOR_ANIMATION_TIME
        else :
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]

    def update(self, horizontal_shift, vertical_shift) :
        self.animate_open()
        self.rect.x += horizontal_shift
        self.rect.y += vertical_shift
