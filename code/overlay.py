import pygame
import config as cg

class Overlay :
    def __init__(self, player) :

        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.broom_surf = pygame.image.load('./graphics/tiles/broom/broom.png').convert_alpha()
        self.broom_rect = self.broom_surf.get_rect(midbottom = cg.BROOM_POSITION)

    def display(self) :
        self.display_surface.blit(self.broom_surf, self.broom_rect)
