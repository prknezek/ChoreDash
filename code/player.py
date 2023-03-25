import pygame
from support import import_folder

class Player(pygame.sprite.Sprite) :
    def __init__(self, pos) :
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.direction = pygame.math.Vector2(0, 0)

    def import_assets(self) :
        self.animations = {'up' : [], 'down' : [], 'left' : [], 'right' : [],
                           'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : []}

        for animation in self.animations.keys() :
            full_path = './graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def get_input(self) :
        # player does not move but shifts tiles around them
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
    
    def move(self, dt) :
        if self.direction.magnitude() > 0 :
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        
    def update(self, dt) :
        self.get_input()
        self.move(dt)