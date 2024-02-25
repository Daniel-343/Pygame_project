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

        color = (255, 255, 255)

        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)

        # defining a font
        small_font = pygame.font.SysFont('Corbel', 35)

        # rendering a text written in
        # this font
        quit_text = small_font.render('quit', True, color)
        play_text = small_font.render('play', True, color)

        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:



        return menu_surface

    def update(self):
        self.display_service.show_menu_surface(self.create_menu())
