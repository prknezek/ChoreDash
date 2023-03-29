import pygame
from pygame.locals import *
import sys
import config as cg
from level import Level
from phone import *
from todolist import todoList
from pause import Pause

class Game :
    def __init__(self) :        
        pygame.init()        
        pygame.key.set_repeat(1000)
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT), SCALED)
        self.clock = pygame.time.Clock() # For setting framerate
        pygame.display.set_caption("ChoreDash")        

        # loading screen here

        self.level = Level()        
        self.phone  = Phone()
        self.todolist = todoList()          
        self.pause = Pause()
        self.font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.bgfont = pygame.font.Font('graphics/5x5.ttf', 15)

    def events(self) :
        # game loop eventssd
        for event in pygame.event.get() :
            # user closes window
            if event.type == pygame.QUIT :
                self.playing = self.running = False
                pygame.quit()
                sys.exit()

    def run(self) :
        # game loop
        while True :
            self.events()

            dt = self.clock.tick(cg.FPS) / 1000            
            self.level.run(dt, self.phone.start_timer)
            self.phone.run(self.screen)
            self.todolist.run(self.screen, self.level.fridge.show_todolist, self.level.completed_array)

            self.pause.run(True)

            pygame.display.update()

if __name__ == "__main__" :
    game = Game()
    game.run()

