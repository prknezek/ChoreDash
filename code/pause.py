import pygame
from pygame.locals import *
import sys
import config as cg
from level import Level
from phone import *
from main import *


class Pause:
    def __init__(self):
        self.show_pause = False
        self.resume_button_rect = pygame.Rect(cg.SCREEN_WIDTH // 2 - 50, cg.SCREEN_HEIGHT // 2 - 25, 100, 50)
        self.font = pygame.font.Font('graphics/Pixeltype.ttf', 25)
    def events(self):
        while self.show_pause:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_pause= not(self.show_pause)
                        if self.show_pause:
                            self.display(cg.SCREEN)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.resume_button_rect.collidepoint(event.pos):
                        self.show_pause = False

    def display(self,screen):
        pause_surface = pygame.Surface((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT))
        pause_surface.set_alpha(150)
        pause_surface.fill((0, 0, 0))

        pygame.draw.rect(pause_surface, (255, 255, 255), self.resume_button_rect)
        resume_text = self.font.render('Resume', True, (0, 0, 0))
        pause_surface.blit(resume_text, (self.resume_button_rect.centerx - resume_text.get_width() // 2, self.resume_button_rect.centery - resume_text.get_height() // 2))

        screen.blit(pause_surface, (0, 0))


        pygame.display.update()
