import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite) :
    def __init__ (self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = FACING_DOWN

        # Sprite
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        # Hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self) :
        pass
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self) :
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a] :
            self.x_change -= PLAYER_SPEED
            self.facing = FACING_LEFT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.x_change += PLAYER_SPEED
            self.facing = FACING_RIGHT
        if keys[pygame.K_UP] or keys[pygame.K_w] :
            self.y_change -= PLAYER_SPEED
            self.facing = FACING_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s] :
            self.y_change += PLAYER_SPEED
            self.facing = FACING_DOWN