import pygame
import sys
import config as cg

class Phone:
    def __init__(self):
        self.show_phone = False
        self.screen = pygame.Surface((cg.SCREEN_WIDTH//4, cg.SCREEN_HEIGHT//2), pygame.SRCALPHA) 
        self.font = pygame.font.Font('graphics/Pixellari.ttf', 30)
        self.phone_image = pygame.image.load('graphics/phone/Phone.png').convert_alpha()
        self.phone_image.set_colorkey((0, 0, 0))
        self.last_time = 0
        self.minutes = 3
        self.seconds = 0
        self.countdown_time = 3 * 60 
        
    def display(self, screen):
        self.screen.blit(self.phone_image, (0, 0))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000: 
            self.last_time = current_time
            self.seconds -= 1
            if self.seconds < 0:
                self.seconds = 59
                self.minutes -= 1
                if self.minutes < 0:
                    self.minutes = 0
                    self.seconds = 0

        if self.countdown_time > 0:
            time_str = f"{self.minutes:02d}:{self.seconds:02d}"
            time_text = self.font.render(time_str, True, (255, 255, 255))
            self.screen.blit(time_text, (20, 20))
        else:
            time_text = self.font.render("TIME'S UP!", True, (255, 0, 0))
            self.screen.blit(time_text, (10, 20))

        screen.blit(self.screen, (50, cg.SCREEN_HEIGHT//2)) 
        pygame.display.flip() 

    def run(self, screen):
        if self.show_phone:
            self.display(screen)
        else:
            return
