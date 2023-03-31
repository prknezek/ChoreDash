import pygame
from pyvidplayer import Video
from gameintro import *


class Intro:
    def __init__(self):
        self.video = Video("./video/test.mp4")
        self.video.set_size((460,330))
        self.gameintro = StayScreen()
        
    def run(self,screen):
        while True:
            self.video.draw(screen, (0,0))
            pygame.display.update()
            if self.video.get_pos() > 14:
                self.gameintro.run(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.playing = self.running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.gameintro.run(screen)
                    self.video.close()
                    return
                
                
                