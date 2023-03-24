import pygame
import sys
from sprites import *
from config import *
from phone import *


class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock() # For setting framerate
        self.running = True
        self.showScreen = False
    

    def create_tile_map(self) :
        for y, row in enumerate(tilemap) :
            for x, column in enumerate(row) :
                if column == "B" :
                    Tile(self, x, y)
                if column == "P" :
                    Player(self, x, y, self.clock)


    def start(self) :
        # a new game starts
        self.playing = True

        # setup sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.tiles = pygame.sprite.LayeredUpdates()

        self.create_tile_map()

    def events(self) :
        # game loop events
        for event in pygame.event.get() :
            # user closes window
            if event.type == pygame.QUIT :
                self.playing = self.running = False
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_e:
            #         self.miniScreen()
                    


    def update(self) :
        # game loop updates
        self.all_sprites.update()

    def draw(self) :
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self) :
        # game loop
        while self.playing :
            self.events()
            self.update()
            self.draw()
        
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

pygame.quit()
sys.exit()