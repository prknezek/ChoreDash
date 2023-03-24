import pygame
import config as cg

class Player(pygame.sprite.Sprite) :
    def __init__(self, pos) :
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.clock = pygame.time.Clock()

        self.speed = 300

    def get_input(self) :
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] :
            self.direction.x = -1
        else :
            self.direction.x = 0
        if keys[pygame.K_UP] or keys[pygame.K_w] :
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s] :
            self.direction.y = 1
        else :
            self.direction.y = 0
        
    def update(self) :
        self.get_input()
        dt = self.clock.tick(cg.FPS) / 1000
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt