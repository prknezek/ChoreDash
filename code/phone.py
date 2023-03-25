import pygame
import sys
import config as cg
from level import Level
from game_data import house



class Phone:
    def __init__(self):
        self.show_phone = True

    def initialize(self):
        pygame.init()
        self.screen = pygame.Surface((cg.SCREEN_WIDTH//4, cg.SCREEN_HEIGHT//2))

    def display(self, screen):
        red = (255, 0, 0)
        rect = pygame.Rect(0, 0, cg.SCREEN_WIDTH//4, cg.SCREEN_HEIGHT//2)
        pygame.draw.rect(self.screen, red, rect) 
        screen.blit(self.screen, (50, cg.SCREEN_HEIGHT//2)) 
        pygame.display.flip() # Update the display  

    def run(self, screen):
 
        self.events() 
        if self.show_phone:
            self.display(screen)
        else:
            return

    def events(self):
        # game loop events
        for event in pygame.event.get():
            # user closes window
            if event.type == pygame.QUIT:
                self.playing = self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show_phone = not self.show_phone # toggle