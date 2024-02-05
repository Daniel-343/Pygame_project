import json

import pygame

from map.MapProvider import MapProvider
from objects.Structure import Structure
from sprites.Sprite import Sprite


class Scene(object):
    def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen

        self.map_layout = self.get_map_layout()
        self.map_provider = MapProvider(32, self.map_layout)
        self.tile_map = self.map_provider.generate_map()

    def show_scene(self):
        clock = pygame.time.Clock()
        tick_rate = 120
        screen_half_width = self.screen_width / 2
        screen_half_height = self.screen_height / 2
        PLAYER_SPEED = 2
        MAP_WIDTH = len(self.map_layout[0]) * 32
        MAP_HEIGHT = len(self.map_layout) * 32
        zoom_scale = 1
        tree = Structure(370, 400, "./objects/object_data/structures/tree.json")
        player = Sprite("./objects/object_data/sprites/player.json", self.screen_width / 2 - 24,
                        self.screen_height / 2 - 24)
        npc = Sprite("./objects/object_data/sprites/player.json", 576, 384)
        stone_arch = Structure(256, 352, "./objects/object_data/structures/stone_arch.json")

        objects = [npc, tree, stone_arch]
        objects.extend(self.get_collidables())
        run = True

        tilemap_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        for drawable in self.tile_map:
            tilemap_surface.blit(drawable.image, drawable.pos)

        internal_surface_size = (2048, 1280)
        internal_surface = pygame.Surface(internal_surface_size, pygame.SRCALPHA)
        internal_surface_size_vector = pygame.math.Vector2(internal_surface_size)
        internal_offset = pygame.math.Vector2(0, 0)
        internal_offset.x = internal_surface_size[0] / 2 - screen_half_width
        internal_offset.y = internal_surface_size[1] / 2 - screen_half_height

        while run:
            objects_above = self.get_objects_above(objects, player)
            objects_below = self.get_objects_below(objects, player)
            image_frame_surface = self.create_image_frame(tilemap_surface, objects_below, objects_above, player,
                                                          MAP_WIDTH, MAP_HEIGHT)

            camera_offset = pygame.math.Vector2(-player.pos.x + screen_half_width - 24,
                                                -player.pos.y + screen_half_height - 24) + internal_offset

            scaled_surface = pygame.transform.scale(internal_surface, internal_surface_size_vector * zoom_scale)
            scaled_rect = scaled_surface.get_rect(center=(screen_half_width, screen_half_height))
            internal_surface.fill('black')
            internal_surface.blit(image_frame_surface, camera_offset)
            self.screen.blit(scaled_surface, scaled_rect)

            player.animate(100)
            npc.animate(100)

            self.check_controls(player, zoom_scale, objects, PLAYER_SPEED)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEWHEEL and 1 < zoom_scale + event.y * 0.03 < 1.7:
                    zoom_scale += event.y * 0.03

            pygame.display.update()

            clock.tick(tick_rate)

    def get_collidables(self):
        collidables = []
        for collidable in self.tile_map:
            if collidable.collision:
                collidables.append(collidable)
        return collidables

    def get_map_layout(self):
        with open('./resources/map1.json', 'r') as file:
            return json.load(file)["map_layout"]

    def get_objects_below(self, objects, player):
        objects_below = []
        for object in objects:
            if object.pos.y + object.collision_area_y >= player.pos.y + player.collision_area_y:
                objects_below.append(object)
        return objects_below

    def get_objects_above(self, objects, player):
        objects_above = []
        for object in objects:
            if object.pos.y + object.collision_area_y <= player.pos.y + player.collision_area_y:
                objects_above.append(object)
        return objects_above

    def create_image_frame(self, tilemap_image, objects_below, objects_above, player, surface_width, surface_height, ):
        image_frame = pygame.Surface((surface_width, surface_height))
        image_frame.blit(tilemap_image, tilemap_image.get_rect())
        for drawable in objects_above:
            image_frame.blit(drawable.image, drawable.pos)
        image_frame.blit(player.image, player.pos)
        for drawable in objects_below:
            image_frame.blit(drawable.image, drawable.pos)

        return image_frame

    def check_controls(self, player, zoom_scale, objects, player_speed):
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
