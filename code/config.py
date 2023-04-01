# GAME SETTINGS
SCREEN_WIDTH = 460
SCREEN_HEIGHT = 330

TILESIZE = 32
FPS = 144

# TILED TILE LAYERS
DECORATION = ['Decoration_1', 'Decoration_2', 'Decoration_3']

LAYERS = {
    'constraints' : 0,
    'black' : 1,
    'floor' : 2,
    'floor_decoration' : 3,
    'walls' : 4,
    'wall_decoration' : 5,
    'furniture' : 6,
    'decoration' : 7,
    'trashcans' : 8,
    'doors' : 9,
    'main' : 10,
    'in_front' : 11,
    'in_front_decoration' : 12,
    'interact_buttons' : 13
}

# DOORS
DOOR_TILE_OFFSET = 6
DOOR_ANIMATION_SPEED = 15

# PLAYER
PLAYER_SPEED = 200
PLAYER_ANIMATION_SPEED = 15
IFRAME_TIME = 3

# INDICATOR
INDICATOR_ANIMATION_SPEED = 2

# LAUNDRY
LAUNDRY_CYCLE_LENGTH = 6
LAUNDRY_ANIMATION_SPEED = 10

# ENEMY
ENEMY_MIN_SPEED = 1
ENEMY_MAX_SPEED = 1.3
ENEMY_SPAWN_INTERVAL = 2
NUM_ENEMIES = 18

# SPONGE
SPONGE_SPEED = 180