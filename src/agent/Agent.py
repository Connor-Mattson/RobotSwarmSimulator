from abc import abstractmethod

class Agent():

    x_pos = 100
    y_pos = 100

    def __init__(self, x, y) -> None:
        self.x_pos = x
        self.y_pos = y
        pass

    def step(self, check_for_world_boundaries = None) -> None:
        pass

    def draw(self, screen) -> None:
        pass