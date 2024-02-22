import pygame


def create_image_frame(tile_map_image, collidables_below, collidables_above, player, surface_width, surface_height, ):
    image_frame = pygame.Surface((surface_width, surface_height))
    image_frame.blit(tile_map_image, tile_map_image.get_rect())
    for drawable in collidables_above:
        image_frame.blit(drawable.image, drawable.pos)
    image_frame.blit(player.image, player.pos)
    for drawable in collidables_below:
        image_frame.blit(drawable.image, drawable.pos)

    return image_frame


class DisplayService:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_half_width = screen_width / 2
        self.screen_half_height = screen_height / 2
        self.internal_surface_size = (2048, 1280)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2(0, 0)
        self.internal_offset.x = self.internal_surface_size[0] / 2 - self.screen_half_width
        self.internal_offset.y = self.internal_surface_size[1] / 2 - self.screen_half_height

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

