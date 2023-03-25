import pygame
import config as cg
from player import Player
from sprites import Generic

class Level :
    def __init__(self) :
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()

        self.setup()

    def setup(self) :
        self.player = Player((320, 240), self.all_sprites)

        # house
        Generic(pos = (0,0),
                surface = pygame.image.load('./graphics/world/house.png').convert_alpha(),
                groups = self.all_sprites,
                z = cg.LAYERS['house'])
        

    def run(self, dt) :
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group) :
    def __init__(self) :
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player) :
        self.offset.x = player.rect.centerx - cg.SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - cg.SCREEN_HEIGHT / 2

        for layer in cg.LAYERS.values() :
            for sprite in self.sprites() :
                if sprite.z == layer :
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
    
