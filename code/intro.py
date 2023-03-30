import pygame
from pyvidplayer import Video


class Intro:
    def __init__(self):
        self.video = Video("./video/test.mp4")
        self.video.set_size((460,330))
        
    def run(self,screen):
        while True:
            self.video.draw(screen, (0,0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.video.close()
                    return
                
                