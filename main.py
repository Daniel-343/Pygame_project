import pygame

from game_data import RouteProvider
from scenes.Scene import Scene


class Main:
    def __init__(self):
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def run(self):
        main_scene = Scene("main_scene", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)
        next_scene = main_scene
        while True:
            next_scene = self.get_scene_by_name(next_scene.show_scene())
        pygame.quit()

    def get_scene_by_name(self, name):
        return Scene(name, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)


if __name__ == "__main__":
    pygame.init()
    main = Main()

    main.run()
