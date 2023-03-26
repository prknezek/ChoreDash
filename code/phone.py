import pygame
import sys
import config as cg
#from settings import *

class Phone:
    def __init__(self):
        self.show_phone = False
        self.screen = pygame.Surface((cg.SCREEN_WIDTH//4, cg.SCREEN_HEIGHT//2))
        self.font = pygame.font.Font('graphics/Pixellari.ttf', 30)

    def display(self, screen):
        red = (255, 0, 0)
        rect = pygame.Rect(0, 0, cg.SCREEN_WIDTH//4, cg.SCREEN_HEIGHT//2)
        pygame.draw.rect(self.screen, red, rect) 
        screen.blit(self.screen, (50, cg.SCREEN_HEIGHT//2)) 
        pygame.display.flip() # Update the display  

    def run(self, screen):
        if self.show_phone:
            self.display(screen)
        else:
            return