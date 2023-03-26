import pygame
import pygame.freetype
import sys
import config as cg
#from settings import *

class Phone:
    def __init__(self):
        
        # options
        self.width = 162
        self.height = 260

        self.show_phone = True
        self.phone_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA) 
        self.font = pygame.font.Font('graphics/Pixeltype.ttf', 15)
        self.phone_image = pygame.transform.scale(pygame.image.load('graphics/phone/Phone.png').convert_alpha(), (self.width, self.height))
        self.phone_image.set_colorkey((0, 0, 0))       

        self.space = 5
        self.padding = 8

        self.left_coord = 30

        self.texts = [
            ("omw home sweetie, be sure u did all the things on the fridge !", "5:10"),
            ("almost home ! ", "5:28"),
            ("note: press tab to close the phone and start the game! ", "5:28")
        ]

        self.initTexts()
    
    def initTexts(self):
        self.text_surfs = []
        for item in self.texts:
            text_surf = self.font.render(item[0], False, 'Black')
            self.text_surfs.append(text_surf)
        self.text_surfs.reverse()

    def display(self, display_surf):        
        # render phone
        self.phone_surf.blit(self.phone_image, (0, 0))
        self.phone_rect = self.phone_surf.get_rect(bottom = cg.SCREEN_HEIGHT, left = self.left_coord)
        display_surf.blit(self.phone_surf, self.phone_rect)
        
        # render texts
        for text_surf_index, text_surf in enumerate(self.text_surfs):
            text_surf_rect = text_surf.get_rect(left = self.left_coord + 15, bottom = cg.SCREEN_HEIGHT - (40 + (text_surf_index * 10)))
            display_surf.blit(text_surf, text_surf_rect)
        
        pygame.display.flip() # Update the display


    def run(self, screen):
        if self.show_phone:
            self.display(screen)
        else:
            return