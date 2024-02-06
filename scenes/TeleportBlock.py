import pygame


class TeleportBlock:
    def __init__(self, destination, initial_position_x, initial_position_y, width, height):
        self.destination = destination
        self.teleport_surface = pygame.Surface((width, height))
        self.pos = self.teleport_surface.get_rect().move(initial_position_x, initial_position_y)

    def check_if_collide(self, player):
        if player.pos.colliderect(self.pos):
            return True
        return False
