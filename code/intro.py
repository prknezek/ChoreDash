import pygame
import sys
from pyvidplayer import Video

class Intro:
    def __init__(self):
        self.video = Video("./video/newFile.mp4")
        self.video.set_size((920,660))
        self.video.set_volume(0.4)

        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load('graphics/UI/cursor.png').convert_alpha()
        self.cursor_img_rect = self.cursor_img.get_rect()
        self.cursor_img_mask = pygame.mask.from_surface(self.cursor_img)


    def displayCursor(self,screen):
        self.cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
        screen.blit(self.cursor_img, self.cursor_img_rect) # draw over it


    def run(self,screen):
        while True:
            
            self.video.draw(screen, (0,0))
            if self.video.get_pos() > 39.5:
                self.video.seek(-10)
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.playing = self.running = False
                    pygame.quit()
                    sys.exit()
                if self.video.get_pos() > 25:
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.video.close()
                        return
            self.displayCursor(screen)
            pygame.display.update()

