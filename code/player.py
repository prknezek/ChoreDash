import pygame
import config as cg
from support import import_folder
from sprites import Door

class Player(pygame.sprite.Sprite) :
    def __init__(self, pos, group, collision_sprites, door_sprites) :
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = cg.LAYERS['main']

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = cg.PLAYER_SPEED

        # collision
        self.hitbox = self.rect.copy().inflate((-20, -40))
        self.collision_sprites = collision_sprites
        self.door_sprites = door_sprites
        #self.image.fill('black')

    def update(self, dt) :
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)

    def import_assets(self) :
        self.animations = {'up' : [], 'down' : [], 'left' : [], 'right' : [],
                           'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : []}

        for animation in self.animations.keys() :
            full_path = './graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt) :
        self.frame_index += cg.PLAYER_ANIMATION_SPEED * dt
        if self.frame_index >= len(self.animations[self.status]) :
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self) :
        # player does not move but shifts tiles around them
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.status = 'right'
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] :
            self.status = 'left'
            self.direction.x = -1
        else :
            self.direction.x = 0

        # vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w] :
            self.status = 'up'
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s] :
            self.status = 'down'
            self.direction.y = 1
        else :
            self.direction.y = 0
    
    def get_status(self) :
        # if player not moving add _idle to status
        if self.direction.magnitude() == 0 :
            self.status = self.status.split('_')[0] + '_idle'

    def collision(self, direction) :
        for sprite in self.collision_sprites.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :
                    # doors have their own collision events so we detect for every other sprite
                    if sprite not in self.door_sprites :
                        if direction == 'horizontal' :
                            # moving right
                            if self.direction.x > 0 :
                                self.hitbox.right = sprite.hitbox.left
                            # moving left
                            if self.direction.x < 0 :
                                self.hitbox.left = sprite.hitbox.right
                            self.rect.centerx = self.hitbox.centerx
                            self.pos.x = self.hitbox.centerx

                        if direction == 'vertical' :
                            # moving up
                            if self.direction.y < 0 :
                                self.hitbox.top = sprite.hitbox.bottom
                            # moving down
                            if self.direction.y > 0 :
                                self.hitbox.bottom = sprite.hitbox.top
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
                    

    def move(self, dt) :
        if self.direction.magnitude() > 0 :
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
        