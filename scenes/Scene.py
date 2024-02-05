import json

import pygame

from game_data import RouteProvider
from map.MapProvider import MapProvider
from objects.Structure import Structure
from sprites.Sprite import Sprite


def check_controls(player, zoom_scale, objects, player_speed):
    key = pygame.key.get_pressed()
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and not player.check_if_collides(objects, -player_speed, 0):
        player.move_left(zoom_scale)
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and not player.check_if_collides(objects, player_speed, 0):
        player.move_right(zoom_scale)
    if (key[pygame.K_DOWN] or key[pygame.K_s]) and not player.check_if_collides(objects, 0, player_speed):
        player.move_down(zoom_scale)
    if (key[pygame.K_UP] or key[pygame.K_w]) and not player.check_if_collides(objects, 0, -player_speed):
        player.move_up(zoom_scale)
    if not any((key[pygame.K_LEFT], key[pygame.K_RIGHT], key[pygame.K_DOWN], key[pygame.K_UP], key[pygame.K_w],
                key[pygame.K_a], key[pygame.K_s], key[pygame.K_d])):
        player.state = "idle"


def get_map_layout(map_layout_source):
    with open(map_layout_source, 'r') as file:
        return json.load(file)["map_layout"]


def get_collidables_below(collidables, player):
    collidables_below = []
    for collidable in collidables:
        if collidable.pos.y + collidable.collision_area_y >= player.pos.y + player.collision_area_y:
            collidables_below.append(collidable)
    return collidables_below


def get_collidables_above(collidables, player):
    collidables_above = []
    for collidable in collidables:
        if collidable.pos.y + collidable.collision_area_y <= player.pos.y + player.collision_area_y:
            collidables_above.append(collidable)
    return collidables_above


def create_image_frame(tile_map_image, collidables_below, collidables_above, player, surface_width, surface_height, ):
    image_frame = pygame.Surface((surface_width, surface_height))
    image_frame.blit(tile_map_image, tile_map_image.get_rect())
    for drawable in collidables_above:
        image_frame.blit(drawable.image, drawable.pos)
    image_frame.blit(player.image, player.pos)
    for drawable in collidables_below:
        image_frame.blit(drawable.image, drawable.pos)

    return image_frame


def get_collidable_tiles(tile_map):
    collidables = []
    for collidable in tile_map:
        if collidable.collision:
            collidables.append(collidable)
    return collidables


def get_collidables(scene_data):
    collidables = []
    for collidable in scene_data["objects"]["structures"]:
        collidables.append(
            Structure(collidable["name"], collidable["initial_position_x"], collidable["initial_position_y"]))
    for collidable in scene_data["objects"]["sprites"]:
        collidables.append(
            Sprite(collidable["name"], collidable["initial_position_x"], collidable["initial_position_y"]))
    return collidables


class Scene(object):
    def __init__(self, screen_width, screen_height, screen, map_name):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.collidables = []

        self.map_layout = get_map_layout(RouteProvider.get_route_by_name(map_name, "map"))
        self.map_provider = MapProvider(32, self.map_layout)
        self.tile_map = self.map_provider.generate_map()

    def show_scene(self, scene_name):
        clock = pygame.time.Clock()
        tick_rate = 120
        screen_half_width = self.screen_width / 2
        screen_half_height = self.screen_height / 2
        player_speed = 2
        map_width = len(self.map_layout[0]) * 32
        map_height = len(self.map_layout) * 32
        zoom_scale = 1

        player = Sprite("player", self.screen_width / 2 - 24,
                        self.screen_height / 2 - 24)

        scene_route = RouteProvider.get_route_by_name(scene_name, "scene")
        with open(scene_route, 'r') as file:
            scene_data = json.load(file)["sceneData"]

        collidables = get_collidables(scene_data)
        collidables.extend(get_collidable_tiles(self.tile_map))
        run = True

        tile_map_surface = pygame.Surface((map_width, map_height))
        for drawable in self.tile_map:
            tile_map_surface.blit(drawable.image, drawable.pos)

        internal_surface_size = (2048, 1280)
        internal_surface = pygame.Surface(internal_surface_size, pygame.SRCALPHA)
        internal_surface_size_vector = pygame.math.Vector2(internal_surface_size)
        internal_offset = pygame.math.Vector2(0, 0)
        internal_offset.x = internal_surface_size[0] / 2 - screen_half_width
        internal_offset.y = internal_surface_size[1] / 2 - screen_half_height

        while run:
            collidables_above = get_collidables_above(collidables, player)
            collidables_below = get_collidables_below(collidables, player)
            image_frame_surface = create_image_frame(tile_map_surface, collidables_below, collidables_above, player,
                                                     map_width, map_height)

            camera_offset = (pygame.math.Vector2(-player.pos.x + screen_half_width - player.pos.width / 2,
                                                 -player.pos.y + screen_half_height - player.pos.height / 2)
                             + internal_offset)

            scaled_surface = pygame.transform.scale(internal_surface, internal_surface_size_vector * zoom_scale)
            scaled_rect = scaled_surface.get_rect(center=(screen_half_width, screen_half_height))
            internal_surface.fill('black')
            internal_surface.blit(image_frame_surface, camera_offset)
            self.screen.blit(scaled_surface, scaled_rect)

            player.animate(100)
            # npc.animate(100)

            check_controls(player, zoom_scale, collidables, player_speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEWHEEL and 1 < zoom_scale + event.y * 0.03 < 1.7:
                    zoom_scale += event.y * 0.03

            pygame.display.update()

            clock.tick(tick_rate)
