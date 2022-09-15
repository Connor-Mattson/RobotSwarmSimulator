from src.gui.abstractGUI import AbstractGUI


class World():

    def __init__(self, w, h):
        self.population = []
        self.behavior = []
        self.bounded_width = 100
        self.bounded_height = 100
        self.gui = None
        self.bounded_height = h
        self.bounded_width = w
        pass
    
    def setup(self):
        pass

    def step(self):
        pass

    def draw(self, screen):
        pass

    def attach_gui(self, gui: AbstractGUI):
        self.gui = gui

    def evaluate(self, steps: int):
        for _ in range(steps):
            self.step()

