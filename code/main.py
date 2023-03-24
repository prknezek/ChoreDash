import pygame
import sys
#from sprites import *
import config as cg
from level import Level
from game_data import house

class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((cg.WIN_WIDTH, cg.WIN_HEIGHT))
        self.clock = pygame.time.Clock() # For setting framerate
        self.running = True
        self.level = Level(house, self.screen)

    def start(self) :
        # a new game starts
        self.playing = True

    def events(self) :
        # game loop events
        for event in pygame.event.get() :
            # user closes window
            if event.type == pygame.QUIT :
                self.playing = self.running = False
                pygame.quit()
                sys.exit()

    def main(self) :
        # game loop
        while self.playing :
            self.events()

            self.screen.fill('black')
            self.level.run()

            pygame.display.update()
            self.clock.tick(cg.FPS)
        
        self.running = False

    def game_over(self) :
        pass

    def intro_screen(self) :
        pass

g = Game()
g.intro_screen()
g.start()
while g.running :
    g.main()
    g.game_over()

