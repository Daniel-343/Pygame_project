import sys

import pygame

from game_data import RouteProvider
from map.MapProvider import MapProvider
from scenes import SceneService
from scenes.TeleportBlock import TeleportBlock
from sprites.Sprite import Sprite
from utils import KeyListener


class Scene(object):
    def __init__(self, scene_name, screen_width, screen_height, screen, area_entry_point_y, area_entry_point_x):
        self.area_entry_point_y = area_entry_point_y
        self.area_entry_point_x = area_entry_point_x
        self.scene_name = scene_name
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.collidables = []
        self.run = True

        self.screen_half_width = self.screen_width / 2
        self.screen_half_height = self.screen_height / 2

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

        internal_surface_size = (2048, 1280)
        internal_surface = pygame.Surface(internal_surface_size, pygame.SRCALPHA)
        internal_surface_size_vector = pygame.math.Vector2(internal_surface_size)
        internal_offset = pygame.math.Vector2(0, 0)
        internal_offset.x = internal_surface_size[0] / 2 - self.screen_half_width
        internal_offset.y = internal_surface_size[1] / 2 - self.screen_half_height

        while self.run:
            collidables_above = SceneService.get_collidables_above(collidables, player)
            collidables_below = SceneService.get_collidables_below(collidables, player)
            image_frame_surface = SceneService.create_image_frame(tile_map_surface, collidables_below,
                                                                  collidables_above, player,
                                                                  map_width, map_height)

            self.show_screen_surface(image_frame_surface, player, internal_surface,
                                     internal_offset, internal_surface_size_vector, zoom_scale)

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

    def show_screen_surface(self, image_frame_surface, player, internal_surface,
                            internal_offset, internal_surface_size_vector, zoom_scale):

        camera_offset = (pygame.math.Vector2(-player.pos.x + self.screen_half_width - player.pos.width / 2,
                                             -player.pos.y + self.screen_half_height - player.pos.height / 2)
                         + internal_offset)

        scaled_surface = pygame.transform.scale(internal_surface, internal_surface_size_vector * zoom_scale)
        scaled_rect = scaled_surface.get_rect(center=(self.screen_half_width, self.screen_half_height))
        internal_surface.fill('black')
        internal_surface.blit(image_frame_surface, camera_offset)
        self.screen.blit(scaled_surface, scaled_rect)
