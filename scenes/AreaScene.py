import sys

import pygame

from map.MapProvider import MapProvider
from scenes import SceneService
from scenes.Scene import Scene
from utils import KeyListener, RouteProvider


class AreaScene(Scene):
    def __init__(self, display_service, scene_name, area_entry_point_y, area_entry_point_x, player, zoom_scale):
        super().__init__(display_service)
        self.scene_data = SceneService.get_scene_data(scene_name)
        self.map_provider = MapProvider(32, self.scene_data["map_name"])
        self.area_entry_point_y = area_entry_point_y
        self.area_entry_point_x = area_entry_point_x
        self.zoom_scale = zoom_scale
        self.player = player

        self.player_speed = 2

        self.collidables = SceneService.get_collidables(self.scene_data, self.map_provider.tile_map)
        self.teleport_blocks = SceneService.create_teleport_blocks(self.scene_data)

        self.image_frame_surface = None
        self.next_area_data = None

    def update(self):
        collidables_above = SceneService.get_collidables_above(self.collidables, self.player)
        collidables_below = SceneService.get_collidables_below(self.collidables, self.player)

        tile_map_surface = self.map_provider.tile_map_surface

        self.image_frame_surface = SceneService.create_image_frame(tile_map_surface, collidables_below,
                                                                   collidables_above, self.player,
                                                                   self.map_provider.map_width,
                                                                   self.map_provider.map_height)

        self.player.animate(100)

        KeyListener.check_controls(self.player, self.zoom_scale, self.collidables, self.player_speed)

        for teleport in self.teleport_blocks:
            if teleport.check_if_collide(self.player):
                self.next_area_data = {
                    "destination": teleport.destination,
                    "area_entry_point_y": teleport.area_entry_point_y,
                    "area_entry_point_x": teleport.area_entry_point_x
                }

