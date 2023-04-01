import pygame
from camera_group import CameraGroup
import config as cg
from random import randint, uniform
from math import atan2, sin, cos

class CleanMinigame :
    def __init__(self, player, player_sprite, collision_sprites) :
        # surfaces & groups
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.sponge_sprite = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # text
        self.font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.bgfont = pygame.font.Font('graphics/5x5.ttf', 15)
        self.live_font = pygame.font.Font('graphics/5x5.ttf', 15)
        self.live_bgfont = pygame.font.Font('graphics/5x5.ttf', 15)

        # spawning
        self.player_sprite = player_sprite
        self.player = player
        self.can_spawn_enemies = True
        self.enemy_spawn_pos = pygame.math.Vector2()
    
        # delay timing
        self.run_delay = False
        self.last_time = 0
        self.seconds = cg.ENEMY_SPAWN_INTERVAL

        # player
        self.teleport_to_start = False        

        self.collision_sprites = collision_sprites

        # game
        self.enemy_spawn_number = cg.NUM_ENEMIES
        self.loss = False
        self.won = False

    # constantly running
    def run(self, dt) :
        # teleporting from x, y = 640, 352
        if not self.teleport_to_start :
            self.teleport_to_start = True
            self.player.pos.x = 1632
            self.player.pos.y = 448

            self.sponge = Sponge(self.player.pos, [self.all_sprites, self.sponge_sprite], self.collision_sprites)

        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.player)
        self.update_spawn_boundaries()
        self.enemy_spawn_delay()
        self.event_detection()
        self.text()
        
    def event_detection(self) :
        if self.can_spawn_enemies :
            self.spawn_enemies()
        
        if len(self.enemy_sprites.sprites()) == 0 and self.enemy_spawn_number == 0 :
            self.won = True
        
        if self.player.lives == 0 and len(self.enemy_sprites.sprites()) != 0 :
            self.loss = True
            for sprite in self.enemy_sprites.sprites() :
                sprite.kill()
        
        if self.won or self.loss :
            self.player.pos.x = 644
            self.player.pos.y = 380
    
    def text(self) :
        text_surf = self.bgfont.render("Lives: ", False, 'Black')
        text_surf_rect = text_surf.get_rect(center = (cg.SCREEN_WIDTH/2 + 1, cg.SCREEN_HEIGHT - 20 + 2))
        self.display_surface.blit(text_surf, text_surf_rect)
        text_surf = self.font.render("Lives: ", False, 'White')
        text_surf_rect = text_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT - 20))
        self.display_surface.blit(text_surf, text_surf_rect)

        live_surf = self.live_bgfont.render(f"                    {self.player.lives}", False, 'Black')
        live_surf_rect = live_surf.get_rect(center = (cg.SCREEN_WIDTH/2 + 1, cg.SCREEN_HEIGHT - 20 + 2))
        self.display_surface.blit(live_surf, live_surf_rect)
        live_surf = self.live_font.render(f"                    {self.player.lives}", False, 'Red')
        live_surf_rect = live_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT - 20))
        self.display_surface.blit(live_surf, live_surf_rect)

    def spawn_enemies(self) :
        if self.enemy_spawn_number > 0 and len(self.enemy_sprites.sprites()) < 4 :
            self.determine_spawn_location()

            Enemy(pos = (self.enemy_spawn_pos.x, self.enemy_spawn_pos.y), 
                group = [self.all_sprites, self.enemy_sprites],
                player_sprite = self.player_sprite,
                player = self.player,
                sponge_sprite = self.sponge_sprite)
            
            self.can_spawn_enemies = False
            self.run_delay = True
            self.enemy_spawn_number -= 1

    def determine_spawn_location(self) :
        self.enemy_spawn_pos.x = randint(self.min_x_spawn_distance, self.max_x_spawn_distance)
        self.enemy_spawn_pos.y = randint(self.min_y_spawn_distance, self.max_y_spawn_distance)
        
    def update_spawn_boundaries(self) :
        top_wall = 224
        bottom_wall = 704
        left_wall = 1280
        right_wall = 2016
        player_radius = 200

        self.max_x_spawn_distance = right_wall
        self.min_x_spawn_distance = left_wall
        self.max_y_spawn_distance = bottom_wall
        self.min_y_spawn_distance = top_wall

        pos_x = int(self.player.pos.x)
        pos_y = int(self.player.pos.y)

        # too close to top
        if pos_y - player_radius < top_wall :
            self.min_y_spawn_distance = pos_y + player_radius
            self.max_y_spawn_distance = bottom_wall
        # too close to bottom
        if pos_y + player_radius > bottom_wall :
            self.min_y_spawn_distance = top_wall
            self.max_y_spawn_distance = pos_y - player_radius
        # too close to right
        if pos_x + player_radius > right_wall :
            self.min_x_spawn_distance = left_wall
            self.max_x_spawn_distance = pos_x - player_radius
        # too close to left
        if pos_x + player_radius < left_wall :
            self.min_x_spawn_distance = pos_x + player_radius
            self.max_x_spawn_distance = right_wall

    def enemy_spawn_delay(self) :
        if not self.run_delay :
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000 :
            self.last_time = current_time
            self.seconds -= 1
            if self.seconds == 0 :
                self.can_spawn_enemies = True
                self.last_time = 0
                self.seconds = cg.ENEMY_SPAWN_INTERVAL

class Enemy(pygame.sprite.Sprite) :
    def __init__(self, pos, group, player_sprite, sponge_sprite, player) :
        super().__init__(group)

        # setup
        image_path = './graphics/tiles/clean_minigame/enemies/' + str(randint(1, 7)) + '.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.z = cg.LAYERS['floor_decoration']

        # movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = uniform(cg.ENEMY_MIN_SPEED, cg.ENEMY_MAX_SPEED)
        self.can_increase_speed = True

        # collision
        self.hitbox = self.rect.copy().inflate((0, 0))
        self.player = player
        self.player_sprite = player_sprite
        self.sponge_sprite = sponge_sprite

    def update(self, dt) :
        self.collision()
        self.move(dt)

    def collision(self) :
        player = self.player_sprite.sprites()[0]
        sponge = self.sponge_sprite.sprites()[0]

        if player.hitbox.colliderect(self.hitbox) and not self.player.iframes :
            # handle player collision
            self.player.lives -= 1
            self.player.iframes = True
        
        if sponge.hitbox.colliderect(self.hitbox) :
            # handle sponge collision
            self.kill()

    def move(self, dt) :
        if self.pos != self.player.pos :                
            stepx = self.player.pos.x - self.pos.x
            stepy = self.player.pos.y - self.pos.y
            avg_step = (abs(stepx) + abs(stepy)) / 2

            # if step gets too small increase speed
            if avg_step < 55 and self.can_increase_speed :
                self.can_increase_speed = False
                self.speed *= 2
            elif not self.can_increase_speed :
                self.can_increase_speed = True
                self.speed /= 2

            # horizontal movement
            self.pos.x += stepx * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx

            # vertical movement
            self.pos.y += stepy * self.speed  * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery

class Sponge(pygame.sprite.Sprite) :
    def __init__(self, pos, group, collision_sprites) :
        super().__init__(group)

        self.z = cg.LAYERS['walls']
        self.image = pygame.image.load('./graphics/tiles/clean_minigame/sponge/sponge.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = cg.SPONGE_SPEED

        self.hitbox = self.rect.copy().inflate((-25, -25))
        self.collision_sprites = collision_sprites

    def update(self, dt) :
        self.input()
        self.move(dt)

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

    def collision(self, direction) :
        for sprite in self.collision_sprites.sprites() :
            if hasattr(sprite, 'hitbox') :
                if sprite.hitbox.colliderect(self.hitbox) :
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

    def input(self) :
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_RIGHT] :
            self.direction.x = 1
        elif keys[pygame.K_LEFT] :
            self.direction.x = -1
        else :
            self.direction.x = 0

        # vertical movement
        if keys[pygame.K_UP] :
            self.direction.y = -1
        elif keys[pygame.K_DOWN] :
            self.direction.y = 1
        else :
            self.direction.y = 0
