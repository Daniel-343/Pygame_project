import pygame


def check_controls(player, zoom_scale, objects, player_speed):
    key = pygame.key.get_pressed()
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and not player.check_if_collides(objects, -player_speed, 0):
        player.move_left(zoom_scale)
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and not player.check_if_collides(objects, player_speed, 0):
        player.move_right(zoom_scale)
    if (key[pygame.K_DOWN] or key[pygame.K_s]) and not player.check_if_collides(objects, 0, player_speed):
        player.move_down(zoom_scale)
    if (key[pygame.K_UP] or key[pygame.K_w]) and not player.check_if_collides(objects, 0, -player_speed):
        player.move_up(zoom_scale)
    if not any((key[pygame.K_LEFT], key[pygame.K_RIGHT], key[pygame.K_DOWN], key[pygame.K_UP], key[pygame.K_w],
                key[pygame.K_a], key[pygame.K_s], key[pygame.K_d])):
        player.state = "idle"