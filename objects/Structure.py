import json

import pygame

from utils import RouteProvider


class Structure:
    def __init__(self, name, initial_position_x, initial_position_y):
        self.data_source = RouteProvider.get_route_by_name(name, "structure")
        self.structure_data = self.get_structure_data()
        self.sheet = self.structure_data["sheet"]
        self.image = self.get_image_by_pixel(self.structure_data["width"], self.structure_data["height"],
                                             self.structure_data["x_dest"], self.structure_data["y_dest"], 1, "black",
                                             "right")
        self.width = self.structure_data["width"]
        self.height = self.structure_data["height"]
        self.pos = self.image.get_rect().move(initial_position_x, initial_position_y)
        self.collision_areas = self.structure_data["collision_areas"]
        self.collision = self.structure_data["collision"]
        self.collision_area_x = self.structure_data["collision_areas"][0]["collision_area_x"]
        self.collision_area_y = self.structure_data["collision_areas"][0]["collision_area_y"]
        self.collision_area_width = self.structure_data["collision_areas"][0]["collision_area_width"]
        self.collision_area_height = self.structure_data["collision_areas"][0]["collision_area_height"]

    def get_image_by_frame(self, width, height, x_frame, y_frame, scale, colour, direction):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((x_frame * width), (y_frame * height), width, height))
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

    def get_image_by_pixel(self, width, height, x_dest, y_dest, scale, colour, direction):
        image = pygame.Surface((width, height)).convert_alpha()
        sheet = pygame.image.load(self.sheet)
        image.blit(sheet, (0, 0), (x_dest, y_dest, width, height))
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

    def get_structure_data(self):
        with open(self.data_source, 'r') as file:
            #print(json.load(file)["structureData"]["collision_areas"][0]["collision_area_x"])
            return json.load(file)["structureData"]

    #def get_collision_areas(self):
