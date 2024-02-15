import pygame

from scenes.Scene import Scene


class Main:
    def __init__(self):
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.area_entry_point_y = 300
        self.area_entry_point_x = 300

    def run(self):
        current_scene = Scene("main_scene", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen,
                              self.area_entry_point_y,
                              self.area_entry_point_x)
        while current_scene:
            scene_data = current_scene.show_scene()
            self.area_entry_point_y = scene_data["area_entry_point_y"]
            self.area_entry_point_x = scene_data["area_entry_point_x"]
            current_scene = self.get_scene_by_name(scene_data["destination"])

    def get_scene_by_name(self, name):
        return Scene(name, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.area_entry_point_y,
                     self.area_entry_point_x)


if __name__ == "__main__":
    pygame.init()
    main = Main()

    main.run()
