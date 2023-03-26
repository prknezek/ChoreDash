import pygame
import sys
import config as cg
#from settings import *

class Phone:
    def __init__(self):
        self.show_phone = False
        self.screen = pygame.Surface((cg.SCREEN_WIDTH//4, cg.SCREEN_HEIGHT//2), pygame.SRCALPHA) 
        self.font = pygame.font.Font('graphics/Pixellari.ttf', 30)
        self.phone_image = pygame.image.load('graphics/phone/Phone.png').convert_alpha()
        self.phone_image.set_colorkey((0, 0, 0))

    def display(self, screen):
        self.screen.blit(self.phone_image, (0, 0))
        screen.blit(self.screen, (50, cg.SCREEN_HEIGHT//2)) 
        pygame.display.flip() # Update the display

    def run(self, screen):
        if self.show_phone:
            self.display(screen)
        else:
            return