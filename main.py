import pygame

from scenes.Scene import Scene


class Main:
    def __init__(self):
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def run(self):
        current_scene = Scene("main_scene", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)
        while current_scene:
            current_scene = self.get_scene_by_name(current_scene.show_scene())

    def get_scene_by_name(self, name):
        return Scene(name, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)


if __name__ == "__main__":
    pygame.init()
    main = Main()

    main.run()
