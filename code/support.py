from csv import reader
from .config import TILESIZE
import pygame

def import_csv_layout(path) :
    tile_map = []
    with open(path) as map :
        # map is csv data
        level = reader(map, delimiter = ',')
        for row in level :
            tile_map.append(list(row))
        return tile_map

def import_cut_graphics(path) :
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILESIZE)
    tile_num_y = int(surface.get_size()[1] / TILESIZE)

    cut_tiles = []
    for row in range(tile_num_y) :
        for col in range(tile_num_x) :
            x = col * TILESIZE
            y = row * TILESIZE

            new_surface = pygame.Surface((TILESIZE, TILESIZE))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            cut_tiles.append(new_surface)

    return cut_tiles