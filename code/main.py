import pygame
from pygame.locals import * 
import sys  
import config as cg
from level import Level
from phone import *
from todolist import todoList
from pause import Pause
from ending import EndScreen
from pygame import mixer
from intro import Intro

class Game :
    def __init__(self) :        
        pygame.init()        
        pygame.key.set_repeat(1000)
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT), SCALED)
        self.clock = pygame.time.Clock() # For setting framerate
        pygame.display.set_caption("ChoreDash")        

        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load('graphics/cursor.png').convert_alpha()
        self.cursor_img_rect = self.cursor_img.get_rect()
        self.cursor_img_mask = pygame.mask.from_surface(self.cursor_img)

        # loading screen here
        #self.intro = Intro()
        self.level = Level()        
        self.phone  = Phone()
        self.todolist = todoList()          
        self.pause = Pause(self.cursor_img.get_width(), self.cursor_img.get_height())
        self.end = EndScreen(self.cursor_img.get_width(), self.cursor_img.get_height())
        self.font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.bgfont = pygame.font.Font('graphics/5x5.ttf', 15)

        #music
        mixer.music.load("./audio/bg.mp3")
        mixer.music.set_volume(0.1)
        

    def events(self) :
        # game loop eventssd
        for event in pygame.event.get() :
            # user closes windows
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        
        if self.phone.is_Timer_Done:
            self.end.show_end = True

        if self.pause.retry_bool or self.end.retry_bool == True:
            self.__init__()

    def displayCursor(self):
        self.cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
        self.screen.blit(self.cursor_img, self.cursor_img_rect) # draw over it

    def run(self) :
        
        # splash screen here with (Hungry Games)

        self.end.show_end = False

        #self.intro.run(self.screen)
        mixer.music.play(-1)
        
        # game loop
        while True :
            if self.pause.retry_bool == True:
                self.__init__()
                
            self.events()
            dt = self.clock.tick(cg.FPS) / 1000            
            self.level.run(dt, self.phone.start_timer and not (self.pause.show_pause or self.end.show_end))
            self.phone.run(self.screen, self.pause.show_pause or self.end.show_end)
            self.todolist.run(self.screen, self.level.fridge.show_todolist, self.level.completed_array)
            self.pause.run(self.cursor_img_mask, not self.end.show_end)            
            self.end.run(self.cursor_img_mask, self.todolist.taskCompletions, self.phone.minutes, self.phone.seconds)
            
            self.displayCursor()

            pygame.display.update()

if __name__ == "__main__" :
    game = Game()    
    game.run()
