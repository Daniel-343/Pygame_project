class Tile(object):
    def __init__(self, image, initial_position_x, initial_position_y, collision):
        self.image = image
        self.pos = image.get_rect().move(initial_position_x, initial_position_y)
        self.collision = collision