class Tile(object):
    def __init__(self, image, initial_position_x, initial_position_y, collision):
        self.image = image
        self.pos = image.get_rect().move(initial_position_x, initial_position_y)
        self.collision = collision
        self.collision_area_x = 0
        self.collision_area_y = 0
        self.collision_area_width = self.pos.width
        self.collision_area_height = self.pos.height
        self.collision_areas = [
            {
                "collision_area_x": 0,
                "collision_area_y": 0,
                "collision_area_width": 32,
                "collision_area_height": 32
            }
        ]
