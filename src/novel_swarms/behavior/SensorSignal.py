import math
from typing import Tuple
import numpy as np
from typing import List
from .AbstractBehavior import AbstractBehavior
import matplotlib.pyplot as plt

class SensorSignalBehavior(AbstractBehavior):

    def __init__(self, history=100, show=True, sensor_index=0):
        super().__init__(name="SensorSignal", history_size=history)
        self.world = None
        self.show = show
        self.index = sensor_index


    def attach_world(self, world):
        self.world = world

    def out_average(self) -> Tuple:
        vals = np.array([0, 0])
        for a in self.world.population:
            history = a.sensors.sensors[self.index].history
            total = sum(history)
            vals += np.array([total, len(history) - total])
        prob = vals / sum(vals)
        print(prob)
        return (self.name, list(prob))

    def calculate(self):
        if len(self.world.highlighted_set) > 0 and self.show:
            plt.ion()
            plt.clf()
            for i, agent in enumerate(self.world.highlighted_set):
                history = agent.sensors.sensors[self.index].history
                plt.subplot(len(self.world.highlighted_set), 1, i + 1)
                x = [self.world.total_steps - len(history) + i for i in range(len(history))]
                plt.plot(x, history, color=tuple([c / 255 for c in agent.body_color]))
                plt.xlabel('Timestep')
                plt.ylabel(f'Logic Signal: Agent {agent.name}')

            plt.show()
            plt.pause(0.001)