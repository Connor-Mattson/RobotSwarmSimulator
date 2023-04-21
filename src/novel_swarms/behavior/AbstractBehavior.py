from typing import Tuple

from numpy import average

class AbstractBehavior():

    def __init__(self, name: str, history_size=100):
        self.name = name
        self.current_value = 0
        self.history_size = history_size
        self.value_history = []

    def set_value(self, value):
        # Keep Track of the [self.history_size] most recent values
        self.value_history.append(value)
        if self.history_size is not None and len(self.value_history) > self.history_size:
            self.value_history = self.value_history[1:]

        self.current_value = value

    def out_current(self) -> Tuple:
        return (self.name, self.value_history[-1])

    def out_average(self) -> Tuple:
        return (self.name, average(self.value_history))

    def reset(self):
        self.current_value = 0
        self.value_history = []

    def draw(self, screen):
        pass