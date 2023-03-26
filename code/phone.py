import pygame
import pygame.freetype
import sys
import config as cg

class Phone:
    def __init__(self):
        
        # options
        self.width = 162
        self.height = 260

        self.show_phone = True
        self.phone_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA) 
        self.font = pygame.font.Font('graphics/Pixeltype.ttf', 15)
        #self.font = pygame.font.SysFont(None, 15)
        self.phone_image = pygame.transform.scale(pygame.image.load('graphics/phone/empty.png').convert_alpha(), (self.width, self.height))
        self.phone_image.set_colorkey((0, 0, 0))       

        self.space = 23 # space between texts
        self.padding = 6 # padding in text bubble
        self.leftrightspace = 7 # space on left and right side of texts

        self.left_coord = 30

        self.texts = [
            ("omw home sweetie, be sure u did all the things on the fridge !", "5:10"),
            ("almost home ! ", "5:28"),
            ("note: press tab to close the phone and start the game! ", "5:28")
        ]
        self.initTexts()

        # making the phone screen borders - updated for bigger phone img
        left = 15
        top = 24
        bottom = 224
        right = 148
        self.phonescreen_rect = pygame.Rect(left, top, right-left, bottom-top)

        # timer
        self.last_time = 0
        self.minutes = 3
        self.seconds = 0
        self.countdown_time = 3 * 60 
    
    def initTexts(self):
        self.totalHeight = 0
        self.text_surfs = []
        for item in self.texts:            
            text_surf = self.font.render(item[0], True, 'Black')
            self.text_surfs.append(text_surf)        
        #self.text_surfs.reverse()

    def showText(self, text_surf, top):
        # white background
        bg_rect = pygame.Rect(self.phonescreen_rect.left + 5,
                              self.phonescreen_rect.top + top + 30,
                              self.phonescreen_rect.width - 20,
                              text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.phone_surf, 'White', bg_rect, 0, 4)

        # show text surf
        text_surf_rect = text_surf.get_rect(midleft = (bg_rect.left + 3, bg_rect.midleft[1]))
        self.phone_surf.blit(text_surf, text_surf_rect)

    def display(self, display_surf):
        #timer
        # display_surf.blit(self.phone_image, (0, 0))

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
            display_surf.blit(time_text, (20, 20))
                

        # render blue background and top bar
        pygame.draw.rect(self.phone_surf, (139,170,220), self.phonescreen_rect)
        pygame.draw.rect(self.phone_surf, (71, 71, 71), pygame.Rect(self.phonescreen_rect.left,self.phonescreen_rect.top,self.phonescreen_rect.width, 20))

        # render phone border
        self.phone_surf.blit(self.phone_image, (0, 0))        

        # render texts
        topOffset = 0
        for text_surf_index, text_surf in enumerate(self.text_surfs):
            # text_surf_rect = text_surf.get_rect(left = 15, bottom = self.height - (text_surf_index * 10))
            # self.phone_surf.blit(text_surf, text_surf_rect)
            self.showText(text_surf, topOffset)
            topOffset += text_surf.get_height() + self.space
        
        contact_text = self.font.render("Mom", True, 'White')
        contact_text_rect = contact_text.get_rect(midbottom = (self.phonescreen_rect.center[0], self.phonescreen_rect.top + 17))
        self.phone_surf.blit(contact_text, contact_text_rect)
        
        # draw phone to actual display
        self.phone_rect = self.phone_surf.get_rect(bottom = cg.SCREEN_HEIGHT, left = self.left_coord)
        display_surf.blit(self.phone_surf, self.phone_rect)
        
        pygame.display.flip() # Update the display


    def run(self, screen):
        if self.show_phone:
            self.display(screen)
        else:
            return
