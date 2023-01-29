class WorldObject:
    def __init__(self, world, detectable=False):
        self.world = world
        self.detectable = detectable

    def draw(self, screen):
        pass

    def step(self):
        pass

    def get_sensing_segments(self):
        return []

    def get_collision_segments(self):
        return []
