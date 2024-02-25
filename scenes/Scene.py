from scenes import SceneService


class Scene:
    def __init__(self, display_service):
        self.display_service = display_service
        self.next_area_data = None

    def update(self):
        pass
