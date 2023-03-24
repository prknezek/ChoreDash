import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite) :
    def __init__(self, size, x, y) :
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))

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
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)

    def animate_open(self) :
        ANIMATION_TIME = 0.15

        if self.frame_index < (len(self.frames) / 2) - 1 :
            self.frame_index += ANIMATION_TIME
        else :
            self.frame_index = 4

        self.image = self.frames[int(self.frame_index)]
    
    def animate_close(self) :
        ANIMATION_TIME = 0.15

        if self.frame_index > 0 :
            self.frame_index -= ANIMATION_TIME
        else :
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]

    def update(self, horizontal_shift, vertical_shift) :
        self.animate_close()
        self.rect.x += horizontal_shift
        self.rect.y += vertical_shift
