import pygame
import pygame.freetype
import config as cg
from itertools import chain

# other code
def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped

def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

class Phone:
    def __init__(self):
        
        # game timer - will update when timer is done
        self.is_Timer_Done = False

        # options
        self.width = 110 # 135
        self.height = 196 # 245

        self.show_phone = True
        self.phone_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA) 
        self.font = pygame.font.Font('graphics/5x5.ttf', 10)
        self.bigfont = pygame.font.Font('graphics/5x5.ttf', 15)
        #self.font = pygame.font.SysFont(None, 15)
        self.phone_image = pygame.transform.scale(pygame.image.load('graphics/phone/phonesprite-2.png').convert_alpha(), (self.width, self.height))
        self.phone_image.set_colorkey((0, 0, 0))       

        self.space = 10 # space between texts
        self.padding = 1 # padding in text bubble
        self.leftrightspace = 7 # space on left and right side of texts

        self.left_coord = 30

        self.start_timer = False
        
        self.button_pressed = False

        # making the phone screen borders - updated for bigger phone img
        self.phonescreen_rect = self.phone_image.get_rect()
        print(self.phonescreen_rect.width, self.phonescreen_rect.height)

        self.texts = [
            ("mom's otw, do the chores !", "5:10"),
            ("check the list on fridge", "5:28"),
            ("press tab to start ! ", "5:28")
        ]

        self.initTexts()

        # timer
        self.last_time = 0
        self.minutes = 1
        self.seconds = 0
        self.countdown_time = 3 * 60 
    
    def initTexts(self):
        self.totalHeight = 0        
        self.all_texts = []
        for item in self.texts:
            self.text_surfs = []
            for line in wrapline(item[0], self.font, 80):
                text_surf = self.font.render(line, True, 'Black')
                self.text_surfs.append(text_surf)
            self.all_texts.append(self.text_surfs)

    def showText(self, text_surf, top):
        # show text surf
        text_surf_rect = text_surf.get_rect(midleft = (15, 31+top))
        self.phone_surf.blit(text_surf, text_surf_rect)

    def tickTimer(self):
        if self.start_timer == False:
            return
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
                    print('TIMER IS UP')
                    self.is_Timer_Done = True
        

    def display(self, display_surf):

        # set rectangle
        self.phone_rect = self.phone_surf.get_rect(bottom = cg.SCREEN_HEIGHT-1, left = self.left_coord)

        # render phone
        self.phone_surf.blit(self.phone_image, (0, 0))        

        # render texts
        topOffset = 0
        for text in self.all_texts:
            for text_surf in text:
                self.showText(text_surf, topOffset)
                topOffset += self.space
            topOffset += 18
        
        # render timer                      
        time_str = f"{self.minutes:02d}:{self.seconds:02d}"        
        time_text = self.bigfont.render("ETA  " + time_str, False, 'White')
        time_text_rect = time_text.get_rect(left = 18, bottom = self.phone_rect.height-32)        
        self.phone_surf.blit(time_text, time_text_rect)

        # draw phone to actual display        
        display_surf.blit(self.phone_surf, self.phone_rect)

        # random vacuum text testing        

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB] and self.button_pressed == False:
            if self.start_timer == False:
                self.start_timer = True
            self.show_phone = not(self.show_phone)
            self.button_pressed = True
        if not keys[pygame.K_TAB]:
            self.button_pressed = False

    def run(self, screen, pause):
        if not pause:
            self.tickTimer()
            self.input()
        if self.show_phone:
            self.display(screen)
        else:
            return
