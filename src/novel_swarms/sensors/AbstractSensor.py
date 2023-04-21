from ..agent.Agent import Agent


class AbstractSensor:
    def __init__(self, parent, static_position=None, n_possible_states=0, draw=True):
        """
        Initialize the abstract class.
            Sensors should typically have a parent that is assigned to them that must be of subclass 'Agent'
            If a parent is not included, a static position is accepted in the form (x, y)
        """
        if parent is not None and not issubclass(type(parent), Agent):
            raise Exception("The parent must be of type Agent")

        self.parent = parent
        self.show = draw
        self.static_position = static_position
        self.n_possible_states = n_possible_states
        self.current_state = 0
        self.detection_id = 0

    def step(self, world):
        if self.parent is None and self.static_position is None:
            raise Exception("Either a parent of type 'Agent' must be provided or a static position in the form (x, y)")
        pass

    def draw(self, screen):
        pass
