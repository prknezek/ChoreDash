import pygame
from pygame.locals import *
import sys
import config as cg
from level import Level
from phone import *
from pause import *

class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT), SCALED)
        self.clock = pygame.time.Clock() # For setting framerate
        pygame.display.set_caption("ChoreDash")
        self.level = Level()
        self.phone  = Phone()     
        self.pause = Pause()   

    def events(self) :
        # game loop events
        for event in pygame.event.get() :
            # user closes window
            if event.type == pygame.QUIT :
                self.playing = self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.phone.show_phone = not(self.phone.show_phone)
                if event.key == pygame.K_ESCAPE:
                    self.pause.show_pause= not(self.pause.show_pause)
                    if(self.pause.show_pause):
                        self.pause.display(self.screen)


    def run(self) :
        # game loop
        while True :
            self.events()
            self.pause.events()
            dt = self.clock.tick(cg.FPS) / 1000
            self.level.run(dt)
            self.phone.run(self.screen)

            pygame.display.update()

if __name__ == "__main__" :
    game = Game()
    game.run()

