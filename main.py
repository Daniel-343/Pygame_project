import pygame

from game_data import RouteProvider
from scenes.Scene import Scene


class Main:
    def __init__(self):
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def run(self):
        scene1 = Scene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, 'main_map')
        scene1.show_scene()
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main = Main()

    main.run()
