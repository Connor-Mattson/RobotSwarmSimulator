import numpy as np


class GeneRule:
    def __init__(self, _max=1.0, _min=-1.0, mutation_step=0.5, round_digits=None, exclude=None):

        if exclude is None:
            self.exclude = []
        else:
            self.exclude = exclude
        self._max = _max
        self._min = _min
        self.round_digits = round_digits
        self._range = self._max - self._min
        self.mutation_step = mutation_step


    def fetch(self):
        if self.round_digits is None:
            return self.getRandomFloat()
        return self.getRandomRoundedFloat()

    def clip(self, value):
        """
        Clips the provided value within the range of the rule, inclusive.
        value ∈ [self._min, self._max]
        """
        if value > self._max:
            return self._max
        if value < self._min:
            return self._min

        for ex_bot, ex_top in self.exclude:
            if ex_bot < value < ex_top:
                dist_to_bot = value - ex_bot
                dist_to_top = ex_top - value
                if dist_to_bot < dist_to_top:
                    value = ex_bot
                else:
                    value = ex_top

        return value

    def getRandomFloat(self):
        return (np.random.rand() * self._range) + self._min

    def getRandomRoundedFloat(self):
        return round(self.getRandomFloat(), self.round_digits)
