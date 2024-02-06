import json

import pygame

from game_data import RouteProvider


class TeleportBlock:
    def __init__(self, destination, initial_position_x, initial_position_y):
        # self.data_source = RouteProvider.get_route_by_name(name, "structure")
        # self.structure_data = self.get_structure_data()

        # self.width = self.structure_data["width"]
        # self.height = self.structure_data["height"]

        self.destination = destination

        self.width = 50
        self.height = 30
        self.teleport_surface = pygame.Surface((self.width, self.height))

        self.pos = self.teleport_surface.get_rect().move(initial_position_x, initial_position_y)

    def check_if_collide(self, player):
        if player.pos.colliderect(self.pos):
            return True
        return False

    # def get_teleport_rect_data(self):
    #     with open(self.data_source, 'r') as file:
    #         #print(json.load(file)["structureData"]["collision_areas"][0]["collision_area_x"])
    #         return json.load(file)["structureData"]
