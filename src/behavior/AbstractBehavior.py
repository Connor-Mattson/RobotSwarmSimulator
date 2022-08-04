from typing import Tuple

from numpy import average

HISTORY_SIZE = 100

class AbstractBehavior():

    name = None
    current_value = 0
    value_history = []
    
    def __init__(self, name: str):
        self.name = name

    def set_value(self, value):
        # Keep Track of the 100 most recent values
        self.value_history.append(value)
        if(len(self.value_history) > HISTORY_SIZE):
            self.value_history = self.value_history[1:]

        self.current_value = value

    def out_current(self) -> Tuple:
        return (self.name, self.value)

    def out_average(self) -> Tuple:
        return (self.name, average(self.value_history))