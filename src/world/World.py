from src.gui.abstractGUI import AbstractGUI

class World():

    population = []
    behavior = []
    bounded_width = 100
    bounded_height = 100
    gui = None

    def __init__(self, w, h):
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