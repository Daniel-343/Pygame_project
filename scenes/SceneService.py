import json

import pygame

from game_data import RouteProvider
from objects.Structure import Structure
from scenes.TeleportBlock import TeleportBlock
from sprites.Sprite import Sprite


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
        if collidable.pos.y + collidable.collision_area_y < player.pos.y + player.collision_area_y:
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


def get_scene_data(scene_name):
    scene_route = RouteProvider.get_route_by_name(scene_name, "scene")
    with open(scene_route, 'r') as file:
        return json.load(file)["sceneData"]


def create_teleport_blocks(scene_data):
    teleport_blocks = []
    for teleport in scene_data["objects"]["teleport_blocks"]:
        teleport_blocks.append(
            TeleportBlock(teleport["destination"], teleport["initial_position_x"], teleport["initial_position_y"],
                          teleport["width"], teleport["height"], teleport["area_entry_point_y"],
                          teleport["area_entry_point_x"]))
    return teleport_blocks
