import pygame
import config as cg

class Generic(pygame.sprite.Sprite) :
    def __init__(self, pos, surface, groups, z = cg.LAYERS['main']) :
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z