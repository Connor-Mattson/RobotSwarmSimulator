from src.agent.Agent import Agent


class AbstractSensor:
    def __init__(self, parent, static_position=None):
        """
        Initialize the abstract class.
            Sensors should typically have a parent that is assigned to them that must be of subclass 'Agent'
            If a parent is not included, a static position is accepted in the form (x, y)
        """
        if parent is not None and not issubclass(type(parent), Agent):
            raise Exception("The parent must be of type Agent")

        if parent is None and static_position is None:
            raise Exception("Either a parent of type 'Agent' must be provided or a static position in the form (x, y)")

        self.parent = parent
        self.static_position = static_position

    def step(self, population):
        pass

    def draw(self, screen):
        pass
