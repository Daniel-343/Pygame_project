import sys

import pygame

from game_data import RouteProvider
from map.MapProvider import MapProvider
from scenes import SceneService
from scenes.Scene import Scene
from sprites.Sprite import Sprite
from utils import KeyListener, DisplayService


class AreaScene(Scene):
    def __init__(self, display_service, scene_name, area_entry_point_y, area_entry_point_x):
        super().__init__(display_service, scene_name)
        self.area_entry_point_y = area_entry_point_y
        self.area_entry_point_x = area_entry_point_x
        self.collidables = []
        self.run = True

        self.scene_data = SceneService.get_scene_data(scene_name)

        self.map_layout = SceneService.get_map_layout(
            RouteProvider.get_route_by_name(self.scene_data["map_name"], "map"))
        self.map_provider = MapProvider(32, self.map_layout)
        self.tile_map = self.map_provider.generate_map()

    def show_scene(self):
        clock = pygame.time.Clock()
        tick_rate = 120

        player_speed = 2
        map_width = len(self.map_layout[0]) * 32
        map_height = len(self.map_layout) * 32
        zoom_scale = 1
        player = Sprite("player", self.area_entry_point_y, self.area_entry_point_x)

        teleport_blocks = SceneService.create_teleport_blocks(self.scene_data)

        collidables = SceneService.get_collidables(self.scene_data)
        collidables.extend(SceneService.get_collidable_tiles(self.tile_map))

        tile_map_surface = pygame.Surface((map_width, map_height))
        for drawable in self.tile_map:
            tile_map_surface.blit(drawable.image, drawable.pos)

        while self.run:
            collidables_above = SceneService.get_collidables_above(collidables, player)
            collidables_below = SceneService.get_collidables_below(collidables, player)
            image_frame_surface = DisplayService.create_image_frame(tile_map_surface, collidables_below,
                                                                    collidables_above, player,
                                                                    map_width, map_height)

            self.display_service.show_scene_surface(image_frame_surface, player, zoom_scale)

            player.animate(100)

            KeyListener.check_controls(player, zoom_scale, collidables, player_speed)

            for teleport in teleport_blocks:
                if teleport.check_if_collide(player):
                    return {
                        "destination": teleport.destination,
                        "area_entry_point_y": teleport.area_entry_point_y,
                        "area_entry_point_x": teleport.area_entry_point_x
                    }

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEWHEEL and 1 < zoom_scale + event.y * 0.03 < 1.7:
                    zoom_scale += event.y * 0.03

            pygame.display.update()

            clock.tick(tick_rate)
        pygame.quit()
        sys.exit()