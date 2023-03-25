# GAME SETTINGS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

TILESIZE = 32
FPS = 60

# TILED TILE LAYERS
FLOOR_DECORATION = ['BedroomFloorDecoration', 'JapaneseFloorDecoration', 'JailFloorDecoration', 'GymFloorDecoration', 'SportsFloorDecoration', 'BathroomFloorDecoration']
WALL_DECORATION = ['LivingRoomWallDecoration', 'KitchenWallDecoration']
FURNITURE = ['KitchenFurniture', 'BedroomFurniture', 'BathroomFurniture', 'LivingRoomFurniture']
DECORATION = ['LivingRoomDecoration', 'KitchenDecoration_1', 'BedroomDecoration', 'BathroomDecoration', 'BirthdayDecoration', 'KitchenDecoration_2']

LAYERS = {
    'black' : 0,
    'floor' : 1,
    'floor_decoration' : 2,
    'walls' : 3,
    'wall_decoration' : 4,
    'furniture' : 5,
    'decoration' : 6,
    'doors' : 7,
    'main' : 8,
    'in_front_bathroom' : 9,
    'in_front_living_room' : 10,
    'constraints' : 11,
}

# DOORS
DOOR_TILE_OFFSET = 6
DOOR_ANIMATION_TIME = 0.15