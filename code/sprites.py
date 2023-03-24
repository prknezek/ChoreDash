import pygame
import config as cg
import math
import random

class Player(pygame.sprite.Sprite) :
    def __init__ (self, game, x, y, clock):
        self.game = game
        self._layer = cg.PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * cg.TILESIZE
        self.y = y * cg.TILESIZE
        self.width = cg.TILESIZE
        self.height = cg.TILESIZE

        self.dt = clock.tick(cg.FPS) / 1000

        self.facing = cg.FACING_DOWN

        # Sprite
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(cg.RED)

        # Hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self) :
        pass
        self.movement()

    def movement(self) :
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a] :
            self.rect.x -= cg.PLAYER_SPEED * self.dt
            self.facing = cg.FACING_LEFT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.rect.x += cg.PLAYER_SPEED * self.dt
            self.facing = cg.FACING_RIGHT
        if keys[pygame.K_UP] or keys[pygame.K_w] :
            self.rect.y -= cg.PLAYER_SPEED * self.dt
            self.facing = cg.FACING_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s] :
            self.rect.y += cg.PLAYER_SPEED * self.dt
            self.facing = cg.FACING_DOWN