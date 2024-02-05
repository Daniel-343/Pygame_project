import json

import pygame

from game_data import RouteProvider


class Sprite(pygame.sprite.Sprite):
    def __init__(self, name, initial_position_x, initial_position_y):
        super().__init__()
        self.data_source = RouteProvider.get_route_by_name(name, "sprite")
        self.sprite_data = self.get_sprite_data()
        self.sheet = self.sprite_data['sheet']
        self.direction = "right"
        self.state = "idle"
        self.idle_animation_frames_right = self.get_animation_frames(0, 3, "right")
        self.idle_animation_frames_left = self.get_animation_frames(0, 3, "left")
        self.running_animation_frames_right = self.get_animation_frames(4, 7, "right")
        self.running_animation_frames_left = self.get_animation_frames(4, 7, "left")
        self.current_frameset = self.idle_animation_frames_right
        self.speed = self.sprite_data['speed']
        self.image = self.get_image(0, 24, 24, 2, "black", "right")
        self.pos = self.image.get_rect().move(initial_position_x, initial_position_y)

        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0

        self.collision_areas = self.sprite_data['collision_areas']
        self.collision_area_y = self.sprite_data['collision_areas'][0]['collision_area_y']

    def move_left(self, multiplier):
        self.state = "running"
        self.direction = "left"
        self.pos = self.pos.move(-self.speed * multiplier, 0)

    def move_right(self, multiplier):
        self.state = "running"
        self.direction = "right"
        self.pos = self.pos.move(self.speed * multiplier, 0)

    def move_up(self, multiplier):
        self.state = "running"
        self.pos = self.pos.move(0, -self.speed * multiplier)

    def move_down(self, multiplier):
        self.state = "running"
        self.pos = self.pos.move(0, self.speed * multiplier)

    def check_if_collides(self, objects, x_direction, y_direction):

        collide = False
        collision_areas = []
        own_collision_area = pygame.Rect(self.pos.x + self.collision_areas[0]['collision_area_x'] + x_direction,
                                         self.pos.y + self.collision_areas[0]['collision_area_y'] + y_direction,
                                         self.collision_areas[0]['collision_area_width'],
                                         self.collision_areas[0]['collision_area_height'])
        for obj in objects:
            for area in obj.collision_areas:
                collision_areas.append(pygame.Rect(obj.pos.x + area['collision_area_x'], obj.pos.y + area['collision_area_y'],
                                                   area['collision_area_width'], area['collision_area_height']))
        for area in collision_areas:
            if area.colliderect(own_collision_area):
                collide = True
        return collide

    def get_image(self, frame, width, height, scale, colour, direction):
        image = pygame.Surface((width, height)).convert_alpha()
        sheet = pygame.image.load(self.sheet)
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
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

    def animate(self, cooldown):
        match self.state:
            case "idle":
                match self.direction:
                    case "right":
                        self.current_frameset = self.idle_animation_frames_right
                    case "left":
                        self.current_frameset = self.idle_animation_frames_left
                    case _:
                        pass
            case "running":
                match self.direction:
                    case "right":
                        self.current_frameset = self.running_animation_frames_right
                    case "left":
                        self.current_frameset = self.running_animation_frames_left
                    case _:
                        pass
            case _:
                pass
        while pygame.time.get_ticks() - self.last_update > cooldown:
            self.image = self.current_frameset[self.frame_index]
            # self.pos = self.image.get_rect().move(self.pos.x, self.pos.y)
            self.frame_index += 1
            self.last_update = pygame.time.get_ticks()
        if self.frame_index >= len(self.current_frameset):
            self.frame_index = 0

    def get_animation_frames(self, first_frame, last_frame, direction):
        frames = []
        for i in range(first_frame, last_frame + 1):
            frames.append(self.get_image(i, 24, 24, 2, "black", direction))
        return frames

    def get_sprite_data(self):
        with open(self.data_source, 'r') as file:
            return json.load(file)["spriteData"]
