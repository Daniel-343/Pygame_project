import random

import pygame

from map.Tile import Tile
from scenes import SceneService
from utils import RouteProvider


class MapProvider(object):
    def __init__(self, tile_size, map_name):
        self.map_layout = SceneService.get_map_layout(
            RouteProvider.get_route_by_name(map_name, "map"))
        self.map_width = len(self.map_layout[0])
        self.map_height = len(self.map_layout)
        self.tile_size = tile_size
        self.map_width = len(self.map_layout[0]) * 32
        self.map_height = len(self.map_layout) * 32
        self.grass_sheet = pygame.image.load("./assets/grass_tileset.png").convert_alpha()
        self.wall_sheet = pygame.image.load("./assets/wall_tileset.png").convert_alpha()
        self.floor_sheet = pygame.image.load("./assets/floor_and_deoratives.png").convert_alpha()
        self.black_tile = pygame.Surface((32, 32)).convert_alpha()
        self.tile_map = self.generate_map()
        self.tile_map_surface = self.generate_tile_map_surface()

    def generate_map(self):
        tile_map = []
        for y_index, y in enumerate(self.map_layout):
            for x_index, x in enumerate(list(y)):
                tile_map.append(self.generate_tile(x, x_index * self.tile_size, y_index * self.tile_size))
        return tile_map

    def generate_tile(self, tile_id, initial_position_x, initial_position_y):
        collision = False
        match tile_id:
            case "s":
                image = self.get_image_by_frame(random.randint(0, 1), random.randint(5, 6), self.grass_sheet, 32, 32, 1,
                                                "black", "right")
            case "f":
                image = self.get_image_by_frame(4, 1, self.floor_sheet, 32, 32, 1,
                                                "black", "right")
            case "g":
                image = self.get_image_by_frame(random.randint(0, 7), random.randint(0, 3), self.grass_sheet, 32, 32, 1,
                                                "black", "right")
            case "b":
                image = self.black_tile
                collision = True
            case _:
                image = pygame.image.load("./assets/brick_wall_32.png").convert_alpha()
        return Tile(image, initial_position_x, initial_position_y, collision)

    def get_image_by_frame(self, x_frame, y_frame, sheet, width, height, scale, colour, direction):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((x_frame * width), (y_frame * height), width, height))
        match direction:
            case "right":
                pass
            case "left":
                image = pygame.transform.flip(image, True, False)
            case _:
                pass
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

    def generate_tile_map_surface(self):
        tile_map_surface = pygame.Surface((self.map_width, self.map_height))
        for drawable in self.tile_map:
            tile_map_surface.blit(drawable.image, drawable.pos)
        return tile_map_surface


