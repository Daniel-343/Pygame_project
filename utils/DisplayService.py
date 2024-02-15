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
