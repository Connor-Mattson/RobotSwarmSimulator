from .AbstractBehavior import AbstractBehavior

class SquarenessBehavior(AbstractBehavior):
    def __init__(self, history=100, archiveMode=False):
        super().__init__(name = "Squareness", history_size=history, archiveMode=archiveMode)
        self.population = None

    def attach_world(self, world):
        self.population = world.population
    
    # Generates values between 0.0 and 1.0
    # 1.0 means the bounding box is a perfect square
    # 0.0 means it's a straight line
    def calculate(self):
        x_coordinates = [agent.x_pos for agent in self.population]
        y_coordinates = [agent.y_pos for agent in self.population]
        bounding_box_width = max(x_coordinates) - min(x_coordinates)
        bounding_box_height = max(y_coordinates) - min(y_coordinates)

        if 0 in (bounding_box_width, bounding_box_height):
            self.set_value(0.0)
        elif bounding_box_width == bounding_box_height:
            self.set_value(1.0)
        elif bounding_box_width > bounding_box_height:
            self.set_value(bounding_box_height / bounding_box_width)
        else:
            self.set_value(bounding_box_width / bounding_box_height)