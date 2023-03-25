import pygame
import config as cg
from player import Player

class Level :
    def __init__(self) :
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()

        self.setup()

    def setup(self) :
        self.player = Player((200, 200), self.all_sprites)

    def run(self, dt) :
        self.display_surface.fill('black')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw()
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group) :
    def __init__(self) :
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self) :
        for sprite in self.sprites() :
            self.display_surface.blit(sprite.image, sprite.rect)
    
