from ..behavior.AbstractBehavior import AbstractBehavior
from typing import Tuple

class SubGroupBehavior(AbstractBehavior):
    def __init__(self, wrapped_behavior: AbstractBehavior, subgroup=0):
        super().__init__(name=f"{wrapped_behavior.name}_{subgroup}", history_size=wrapped_behavior.history_size)
        self.group=subgroup
        self.population=[]

        wrapped_behavior.name = f"{wrapped_behavior.name}_{subgroup}"
        self.wrapped_b = wrapped_behavior


    def attach_world(self, world):
        self.population = []
        self.wrapped_b.attach_world(world)
        for p in world.population:
            if p.group == self.group:
                self.population.append(p)
        self.wrapped_b.population = self.population

    def calculate(self):
        self.wrapped_b.calculate()

    def out_current(self) -> Tuple:
        return self.wrapped_b.out_current()

    def out_average(self) -> Tuple:
        return self.wrapped_b.out_average()