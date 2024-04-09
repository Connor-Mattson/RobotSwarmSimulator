import numpy as np
import math
from .RadialVariance import RadialVarianceBehavior


class RadialVarianceHelper(RadialVarianceBehavior):
    def __init__(self, history=100, regularize=False, name=None):
        if regularize:
            raise NotImplementedError
        super().__init__(history=history, regularize=False)
        self.name = self.__class__.__name__ if name is None else name

    def _calculate(self):
        pass

    def calculate(self):
        self.set_value(self._calculate())


class Fatness2(RadialVarianceHelper):
    @staticmethod
    def distance(a, b):
        return np.linalg.norm(a - b)

    def _calculate(self):
        # calculate average position of all agents
        mu = self.center_of_mass()

        # calculate distance of each agent to mu, save the largest and smallest
        distances = [self.distance(agent.getPosition(), mu) for agent in self.population]
        rmin = np.min(distances)
        rmax = np.max(distances)

        # calculate Fatness but opposite (0 is fat, 1 is perfect circle formation)
        return (rmin ** 2) / (rmax ** 2)


class Fatness(Fatness2):
    def _calculate(self):
        # calculate Fatness (eq(6) from C. Taylor, The impact of catastrophic collisions..., 2021)
        return 1 - super()._calculate()


class Tangentness(RadialVarianceHelper):
    @staticmethod
    def tangentness_inner(agent, mu):
        # inner part of tangentness sum, inside the |abs|
        '''
            p = agent.getPosition()
            d = p - mu
            dnorm = np.linalg.norm(d)
            d = np.zeros(2) if dnorm == 0 else d / np.linalg.norm(d)

            v = agent.getVelocity()
            vnorm = np.linalg.norm(v)
            v = np.zeros(2) if vnorm == 0 else v / vnorm

            return abs(np.dot(d, v))
        '''
        p = agent.getPosition()
        theta = agent.get_heading()
        d = p - mu
        # dnorm = np.linalg.norm(d)
        # d = np.zeros(2) if dnorm == 0 else d / np.linalg.norm(d)
        d_x, d_y = d
        beta = math.atan2(d_y, d_x)
        alpha = theta - beta
        return abs(math.cos(alpha))

    def _calculate(self):
        # calculate average position of all agents
        mu = self.center_of_mass()
        n = len(self.population)

        # calculate Tangentness
        return np.sum([self.tangentness_inner(agent, mu) for agent in self.population]) / n


class Circliness(RadialVarianceHelper):
    def __init__(self, history=100, avg_history_max=100, regularize=False, name=None):
        if regularize:
            raise NotImplementedError
        self.tangentness = Tangentness(history=avg_history_max, regularize=False)
        self.fatness = Fatness(history=avg_history_max, regularize=False)
        super().__init__(history=history, regularize=regularize, name=name)

    def attach_world(self, world):
        self.population = world.population
        self.world_radius = world.config.radius

    @property
    def population(self):
        return self.tangentness.population

    @population.setter
    def population(self, x):
        self.tangentness.population = x
        self.fatness.population = x

    @property
    def world_radius(self):
        return self.tangentness.world_radius

    @world_radius.setter
    def world_radius(self, x):
        self.tangentness.world_radius = x
        self.fatness.world_radius = x

    def _calculate(self):
        _, tau_ = self.tangentness.out_average()
        _, phi_ = self.fatness.out_average()

        return 1 - max(phi_, tau_)

    def calculate(self):
        self.tangentness.calculate()
        self.fatness.calculate()

        self.set_value(self._calculate())