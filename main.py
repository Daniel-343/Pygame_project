import pygame


#from scenes.menu.MainMenuScene import MainMenuScene
from utils.DisplayService import DisplayService


class Main:
    def __init__(self):
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.area_entry_point_y = 300
        self.area_entry_point_x = 300
        self.display_service = DisplayService(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def run(self):
        self.display_service.run()


if __name__ == "__main__":
    pygame.init()
    main = Main()

    main.run()
