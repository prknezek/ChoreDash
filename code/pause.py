import pygame
import config as cg

class Buttons(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.buttons_only_surf = pygame.transform.scale(pygame.image.load('graphics/pausebuttonsonly.png').convert_alpha(), (self.WIDTH, self.HEIGHT))
        self.buttons_mask = pygame.mask.from_surface(self.buttons_only_surf)

class Pause:
    def __init__(self):
        
        # adjustable options
        SIZE_MULTIPLIER = 7
        self.WIDTH = 50 * SIZE_MULTIPLIER
        self.HEIGHT = 33 * SIZE_MULTIPLIER
        self.pause_text_top_offset = 38
        self.smalltext_spacing_from_mid = 32
        self.smalltext_bottom_offset = 45

        # critical variables
        self.show_pause = False
        self.pause_surf = pygame.transform.scale(pygame.image.load('graphics/pause.png').convert_alpha(), (self.WIDTH, self.HEIGHT))        
        self.font = pygame.font.Font('graphics/5x5.ttf', 70)
        self.smfont = pygame.font.Font('graphics/5x5.ttf', 20)

        # self.resume_button_rect = pygame.Rect(cg.SCREEN_WIDTH // 2 - 50, cg.SCREEN_HEIGHT // 2 - 25, 100, 50)

        # other
        self.display_surface = pygame.display.get_surface()
        self.button_pressed = False        
        

    def events(self):
        return

    def display(self, screen):
        bg_surf = pygame.Surface((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT))
        bg_surf.set_alpha(150)
        bg_surf.fill((0, 0, 0))        
        
        paused_text = self.font.render('Pause', False, 'White')
        paused_text_rect = paused_text.get_rect(center = (self.pause_surf.get_width() / 2 + 3, self.pause_text_top_offset))
        self.pause_surf.blit(paused_text, paused_text_rect)

        retry_text = self.smfont.render('Retry', False, 'Black')
        retry_text_rect = retry_text.get_rect(midright = (self.pause_surf.get_width() / 2 - self.smalltext_spacing_from_mid+3, self.pause_surf.get_height() - self.smalltext_bottom_offset))
        self.pause_surf.blit(retry_text, retry_text_rect)

        resume_text = self.smfont.render('Resume', False, 'Black')
        resume_text_rect = resume_text.get_rect(midleft = (self.pause_surf.get_width() / 2 + self.smalltext_spacing_from_mid, self.pause_surf.get_height() - self.smalltext_bottom_offset))
        self.pause_surf.blit(resume_text, resume_text_rect)

        screen.blit(bg_surf, (0,0))
        pause_surf_rect = self.pause_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT/2))
        screen.blit(self.pause_surf, pause_surf_rect)

    def run(self):
        self.input()
        if self.show_pause == True:            
            self.display(self.display_surface)
        else:            
            return

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and self.button_pressed == False:
            self.show_pause = not(self.show_pause)
            self.button_pressed = True
        if not keys[pygame.K_ESCAPE]:
            self.button_pressed = False