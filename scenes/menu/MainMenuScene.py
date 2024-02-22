import sys

import pygame
from pygame import Surface

from scenes.Scene import Scene


class MainMenuScene(Scene):
    def __init__(self, display_service, screen_width, screen_height):
        super().__init__(display_service)
        self.display_service = display_service
        self.screen_width = screen_width
        self.screen_height = screen_height

    def create_menu(self):
        menu_surface = pygame.Surface((self.screen_width, self.screen_height))
        menu_surface.fill('black')
        return menu_surface

    def show_scene(self):
        while self.run:
            clock = pygame.time.Clock()
            tick_rate = 120
            self.display_service.show_menu_surface(self.create_menu())
            if not self.run:
                return {
                    "destination": "main_scene",
                    "area_entry_point_y": 300,
                    "area_entry_point_x": 300
                }
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()
            clock.tick(tick_rate)

        pygame.quit()
        sys.exit()
