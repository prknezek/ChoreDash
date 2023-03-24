from csv import reader
import config as cg
from os import walk
import pygame

def import_folder(path) :
    # path is path to a folder of images for animated tiles
    surface_list = []

    for _, __, image_files in walk(path) :
        for image in image_files :
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list

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
    tile_num_x = int(surface.get_size()[0] / cg.TILESIZE)
    tile_num_y = int(surface.get_size()[1] / cg.TILESIZE)

    cut_tiles = []
    for row in range(tile_num_y) :
        for col in range(tile_num_x) :
            x = col * cg.TILESIZE
            y = row * cg.TILESIZE

            new_surface = pygame.Surface((cg.TILESIZE, cg.TILESIZE))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, cg.TILESIZE, cg.TILESIZE))
            cut_tiles.append(new_surface)

    return cut_tiles