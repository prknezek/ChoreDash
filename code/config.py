# GAME SETTINGS
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400

TILESIZE = 32
FPS = 60

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
    'doors' : 8,
    'main' : 9,
    'in_front' : 10,
    'in_front_decoration' : 11
}

# DOORS
DOOR_TILE_OFFSET = 6
DOOR_ANIMATION_SPEED = 4
# self.offset_x(20) when door opens to left

# PLAYER
PLAYER_SPEED = 200
PLAYER_ANIMATION_SPEED = 15