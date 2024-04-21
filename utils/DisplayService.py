import sys

import pygame

from scenes.AreaScene import AreaScene
from scenes.menu.MainMenuScene import MainMenuScene
from sprites.Sprite import Sprite


class DisplayService:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_half_width = screen_width / 2
        self.screen_half_height = screen_height / 2
        self.internal_surface_size = (2048, 1280)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2(0, 0)
        self.internal_offset.x = self.internal_surface_size[0] / 2 - self.screen_half_width
        self.internal_offset.y = self.internal_surface_size[1] / 2 - self.screen_half_height

    def run(self):
        run = True
        clock = pygame.time.Clock()
        tick_rate = 120
        zoom_scale = 1
        area_entry_point_y = 300
        area_entry_point_x = 300
        player = Sprite("player", area_entry_point_y, area_entry_point_x)
        current_scene = AreaScene(self, "main_scene", area_entry_point_y, area_entry_point_x, player, zoom_scale)
        #current_scene = MainMenuScene(self, self.screen_width, self.screen_height)
        while run:
            current_scene.update()
            if isinstance(current_scene, MainMenuScene):
                self.show_menu_surface(current_scene.create_menu())
            if isinstance(current_scene, AreaScene):
                self.show_scene_surface(current_scene.image_frame_surface, player, zoom_scale)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEWHEEL and 1 < zoom_scale + event.y * 0.03 < 1.7:
                    zoom_scale += event.y * 0.03
                    current_scene.zoom_scale += event.y * 0.03

            if current_scene.next_area_data:
                player.pos.y = current_scene.next_area_data['area_entry_point_y']
                player.pos.x = current_scene.next_area_data['area_entry_point_x']
                current_scene = self.get_scene_by_name(current_scene.next_area_data['destination'],
                                                       current_scene.next_area_data['area_entry_point_y'],
                                                       current_scene.next_area_data['area_entry_point_x'], player,
                                                       zoom_scale)

            pygame.display.update()

            clock.tick(tick_rate)
        pygame.quit()
        sys.exit()

    def show_scene_surface(self, image_frame_surface, player, zoom_scale):

        camera_offset = (pygame.math.Vector2(-player.pos.x + self.screen_half_width - player.pos.width / 2,
                                             -player.pos.y + self.screen_half_height - player.pos.height / 2)
                         + self.internal_offset)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * zoom_scale)
        scaled_rect = scaled_surface.get_rect(center=(self.screen_half_width, self.screen_half_height))
        self.internal_surface.fill('black')
        self.internal_surface.blit(image_frame_surface, camera_offset)
        self.screen.blit(scaled_surface, scaled_rect)

    def show_menu_surface(self, menu_surface):
        menu_rect = menu_surface.get_rect()
        self.screen.blit(menu_surface, menu_rect)

    def get_scene_by_name(self, name, area_entry_point_y, area_entry_point_x, player, zoom_scale):
        return AreaScene(self, name, area_entry_point_y,
                         area_entry_point_x, player, zoom_scale)
