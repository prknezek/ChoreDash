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
    
    def loading(self):
        print("loading")
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH*2, cg.SCREEN_HEIGHT*2))
        surf = pygame.Surface((cg.SCREEN_WIDTH*2, cg.SCREEN_HEIGHT*2))        
        surf.fill((0, 0, 0))
        loading_text = self.bigfont.render("Loading...", False, 'White')
        loading_text_rect = loading_text.get_rect(bottomleft = (20, cg.SCREEN_HEIGHT*2 - 15))
        surf.blit(loading_text, loading_text_rect)
        self.screen.blit(surf, (0,0))
        pygame.display.flip()
        pygame.time.delay(500)
        print("done loading")

    retry = False

    def __init__(self) :        
        pygame.init()        
        pygame.key.set_repeat(1000)
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT), SCALED)
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH*2, cg.SCREEN_HEIGHT*2))
        self.clock = pygame.time.Clock() # For setting framerate
        pygame.display.set_caption("ChoreDash")        

        icon = pygame.image.load('graphics/UI/icon.png').convert_alpha()
        pygame.display.set_icon(icon)

        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load('graphics/UI/cursor.png').convert_alpha()
        self.cursor_img_rect = self.cursor_img.get_rect()
        self.cursor_img_mask = pygame.mask.from_surface(self.cursor_img)

        # loading screen here        
        self.bigfont = pygame.font.Font('graphics/5x5.ttf', 25)        
        self.loading()        
        self.level = Level()        
        self.phone  = Phone()
        self.todolist = todoList()          
        self.pause = Pause(self.cursor_img.get_width(), self.cursor_img.get_height())
        self.end = EndScreen(self.cursor_img.get_width(), self.cursor_img.get_height())        
        self.font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.bgfont = pygame.font.Font('graphics/5x5.ttf', 15)

        print("done setup")

        if not self.retry:
            self.intro = Intro()                        
            #music
            mixer.music.load("./audio/bg.mp3")
            mixer.music.set_volume(0.1)
            self.retry = True
        else:
            self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT), SCALED)
            mixer.music.play(-1)
        

    def events(self) :
        # game loop events

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        
        if self.phone.is_Timer_Done or self.todolist.allTasksCompleted:
            self.end.show_end = True

        if self.pause.retry_bool or self.end.retry_bool == True:
            mixer.music.stop()
            self.__init__()

    def displayCursor(self):
        self.cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
        self.screen.blit(self.cursor_img, self.cursor_img_rect) # draw over it

    def run(self) :
        
        # splash screen here with (Hungry Games)        

        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH*2, cg.SCREEN_HEIGHT*2))        
        self.intro.run(self.screen)
        self.loading()
        self.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT), SCALED)
        mixer.music.play(-1)
        
        # game loop
        while True :
                
            self.events()
            dt = self.clock.tick(cg.FPS) / 1000            
            self.level.run(dt, self.phone.start_timer and not (self.pause.show_pause or self.end.show_end))
            self.phone.run(self.screen, self.pause.show_pause or self.end.show_end)
            self.todolist.run(self.screen, self.level.fridge.show_todolist, self.level.completed_array)
            self.pause.run(self.cursor_img_mask, not self.end.show_end)            

            totalseconds = self.phone.total_minutes*60 + self.phone.total_seconds
            timeleft = self.phone.minutes*60 + self.phone.seconds
            timetoshow = totalseconds - timeleft
            minutes = timetoshow//60
            seconds = timetoshow%60

            self.end.run(self.cursor_img_mask, self.todolist.taskCompletions, minutes, seconds)
            
            self.displayCursor()

            pygame.display.update()

if __name__ == "__main__" :
    game = Game()    
    game.run()
