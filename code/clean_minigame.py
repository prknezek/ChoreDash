import pygame
from camera_group import CameraGroup
import config as cg
from random import randint, uniform

class CleanMinigame :
    def __init__(self, player, player_sprite) :
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        # spawning
        self.player_sprite = player_sprite
        self.player = player
        self.can_spawn_enemies = True
        self.enemy_spawn_pos = pygame.math.Vector2()
    
        # delay timing
        self.run_delay = False
        self.last_time = 0
        self.seconds = cg.ENEMY_SPAWN_INTERVAL

        # teleport
        self.teleport_to_start = False

    # constantly running
    def run(self, dt) :
        # teleporting from x, y = 640, 352
        if not self.teleport_to_start :
            self.teleport_to_start = True
            self.player.pos.x = 1632
            self.player.pos.y = 448

        self.update_spawn_boundaries()
        self.enemy_spawn_delay()
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.player)

        if self.can_spawn_enemies :
            self.spawn_enemies()

    def spawn_enemies(self) :
        self.determine_spawn_location()

        Enemy(pos = (self.enemy_spawn_pos.x, self.enemy_spawn_pos.y), 
              group = self.all_sprites, 
              player_sprite = self.player_sprite,
              player = self.player)
        
        self.can_spawn_enemies = False
        self.run_delay = True

    def determine_spawn_location(self) :
        spawn_side = randint(1, 4)

        match spawn_side :
            case 1 : # top
                self.enemy_spawn_pos.y = randint(self.max_top_y, self.min_top_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.max_right_x)
            case 2 : # bottom
                self.enemy_spawn_pos.y = randint(self.min_bottom_y, self.max_bottom_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.max_right_x)
            case 3 : # left
                self.enemy_spawn_pos.y = randint(self.max_top_y, self.max_bottom_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.min_left_x)
            case 4 : # right
                self.enemy_spawn_pos.y = randint(self.max_top_y, self.max_bottom_y)
                self.enemy_spawn_pos.x = randint(self.max_left_x, self.max_right_x)

        print('enemy pos:')
        print(self.enemy_spawn_pos.x, self.enemy_spawn_pos.y)
        
    def update_spawn_boundaries(self) :
        pos_x = int(self.player.pos.x)
        pos_y = int(self.player.pos.y)

        max_spawn_distance = 250
        min_spawn_distance = 200

        self.max_right_x = pos_x + max_spawn_distance
        self.min_right_x = pos_x + min_spawn_distance
        self.max_left_x = pos_x - max_spawn_distance
        self.min_left_x = pos_x - min_spawn_distance

        self.max_bottom_y = pos_y + max_spawn_distance
        self.min_bottom_y = pos_y + min_spawn_distance
        self.max_top_y = pos_y - max_spawn_distance
        self.min_top_y = pos_y - min_spawn_distance

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
    def __init__(self, pos, group, player_sprite, player) :
        super().__init__(group)

        # setup
        image_path = './graphics/tiles/clean_minigame/enemies/' + str(randint(1, 7)) + '.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.z = cg.LAYERS['main']

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = uniform(cg.ENEMY_MIN_SPEED, cg.ENEMY_MAX_SPEED)
        self.can_increase_speed = True

        # collision
        self.hitbox = self.rect.copy().inflate((0, 0))
        self.player = player
        self.player_sprite = player_sprite

    def update(self, dt) :
        self.player_collision()
        self.move(dt)

    def player_collision(self) :
        player = self.player_sprite.sprites()[0]
        if player.hitbox.colliderect(self.hitbox) :
            # handle collision
            #print('collided with player')
            pass

    def move(self, dt) :
        if self.pos != self.player.pos :
            if self.direction.magnitude() > 0 :
                self.direction = self.direction.normalize()
                
            stepx = self.player.pos.x - self.pos.x
            stepy = self.player.pos.y - self.pos.y
            avg_step = (abs(stepx) + abs(stepy)) / 2

            # if step gets too small increase speed
            if avg_step < 55 and self.can_increase_speed :
                self.can_increase_speed = False
                self.speed *= 2

            # horizontal movement
            self.pos.x += stepx * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx

            # vertical movement
            self.pos.y += stepy * self.speed  * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery