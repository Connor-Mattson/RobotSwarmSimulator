from abc import ABC

class AbstractInitialization(ABC):
    """
    AbstractInitialization: An abstract agent initialization class that allows for abstract parameter typing
    """
    def __init__(self):
        pass

    def set_to_world(self, world):
        """
        Set the initialization of the world agents.
        """
        if not hasattr(self, "positions"):
            raise Exception("Abstract Initialization Class must have the 'positions' attributes assigned")

        for i in range(len(world.population)):
            world.population[i].set_pos_vec(self.positions[i])

    def draw(self, screen):
        pass