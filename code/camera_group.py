import pygame
import config as cg

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