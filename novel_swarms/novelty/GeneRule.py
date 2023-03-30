import random
import numpy as np


class GeneBuilder:
    def __init__(self,
                 rules=None,
                 require_single_elem_gt=None,
                 require_magnitude_gt=None,
                 round_to_digits=None,
                 heuristic_validation=False,
                 ):

        if rules is None or not isinstance(rules, list) or len(rules) == 0:
            print(rules)
            raise Exception("Gene Rules with length > 0 must be provided to an instantiation of GeneBuilder")
        if not isinstance(rules[0], GeneRule):
            raise Exception("Elements of GeneRules parameter must be instances of GeneRule")
        if require_magnitude_gt and require_single_elem_gt:
            raise Exception("Either require_magnitude_gt or require_single_elem_gt may be set -- not both.")

        self.rules = rules
        self.elem_gt = require_single_elem_gt
        self.magnitude_gt = require_magnitude_gt
        self.round_to_digits = round_to_digits
        self.heuristic_validation = heuristic_validation

    def fetch_random_genome(self):
        ret = [rule.fetch() for rule in self.rules]
        while not self.is_valid(ret):
            ret = [rule.fetch() for rule in self.rules]
        if self.round_to_digits is not None:
            for i, elem in enumerate(ret):
                ret[i] = round(elem, self.round_to_digits)
        return ret

    def is_valid(self, controller):
        if not self.heuristic_validation:
            return True
        v0_l, v0_r = controller[0], controller[1]
        v1_l, v1_r = controller[2], controller[3]
        v0_l, v0_r, v1_l, v1_r = round(v0_l, 1), round(v0_r, 1), round(v1_l, 1), round(v1_r, 1)

        k = 0.5
        max_elem_score = max(-min(controller), max(controller))
        max_elem_score = -max_elem_score if max_elem_score < k else max_elem_score

        k_2 = 0.75
        magnitude_score = np.linalg.norm(controller)
        magnitude_score = -magnitude_score if magnitude_score < k_2 else magnitude_score

        k_3 = 0.3
        average_score = np.average(np.sqrt(np.power(controller, 2)))
        average_score = -average_score if average_score < k_3 else average_score

        # Sensor off magnitude (trial i)
        on_magnitude = (v0_l ** 2) + (v0_r ** 2)

        # Sensor on magnitude (trial i)
        off_magnitude = (v1_l ** 2) + (v1_r ** 2)

        # Spinning Detection (sensor off - trial ii)
        if v0_l == 0.0 and v0_r == 0.0:
            off_spin_variance = 1
        else:
            denom = v0_l if v0_l != 0.0 else v0_r
            off_spin_variance = min(abs((v0_l + v0_r) / denom), 1.0)

        # Spinning Detection (sensor on - trial ii)
        if v1_l == 0.0 and v1_r == 0.0:
            on_spin_variance = 0.0
        else:
            denom = v1_l if v1_l != 0.0 else v1_r
            on_spin_variance = min(abs((v1_l + v1_r) / denom), 1)

        # Mirror Property
        mirrored_controller = np.array([v0_l, v0_r, -v0_l, -v0_r])
        mirror_score = np.linalg.norm(mirrored_controller - np.array([v0_l, v0_r, v1_l, v1_r]))
        k_m = 0.3
        mirror_score = -5 if mirror_score < k_m else mirror_score

        # Independence Property
        independent_controller = np.array([v0_l, v0_r, v0_l, v0_r])
        indep = np.linalg.norm(independent_controller - np.array([v0_l, v0_r, v1_l, v1_r]))

        attributes = [
            indep,
            mirror_score,
            on_spin_variance,
            off_spin_variance,
            on_magnitude,
            off_magnitude,
            max_elem_score,
            magnitude_score,
            average_score,
        ]

        # weights = [5.3943, 4.5802, 3.3803, 1.7969, -4.1899, -3.9899, -7.3916, 2.5855, 10.1178]
        weights = [0.8993, 0.7878, 1.7404, 0.7404, 0.4437, 0.3982, -0.1233, 0.0905, 1.1693]
        mx = np.dot(np.array(attributes), np.array(weights))
        # return mx > 10.5
        return mx > 3.8

    def round_to(self, vec):
        if not self.round_to_digits:
            return vec
        ret = vec
        for i, elem in enumerate(ret):
            ret[i] = round(elem, self.round_to_digits)
        return ret

    def validate(self, vec):
        ret = self.valid_element(self.valid_magnitude(vec))
        for i, elem in enumerate(ret):
            ret[i] = round(elem, self.round_to_digits)
        return ret

    def valid_magnitude(self, vec):
        if self.magnitude_gt:
            while self.magnitude(vec) < self.magnitude_gt:
                for i in range(len(vec)):
                    vec[i] += 0.01
        return vec

    def valid_element(self, vec):
        vec = np.array(vec)
        if self.elem_gt and (max(vec) < self.elem_gt):
            if min(vec) > -self.elem_gt and max(vec) < self.elem_gt:
                if -self.elem_gt - min(vec) < self.elem_gt - max(vec):
                    target = min(vec)
                else:
                    target = max(vec)
                ind = np.where(vec == target)[0][0]
                vec[ind] = self.elem_gt
        return vec

    def magnitude(self, vec):
        return np.linalg.norm(np.array(vec))


# class AbstractNucleotide:
#     def mutate_with_chance(self, c=0.2, allow_negation=False):
#         pass

class GeneRule:
    def __init__(self, discrete_domain, step_size=1, allow_mutation=True):
        self.domain = discrete_domain
        self.step = step_size
        self.allow_mutation = allow_mutation

    def fetch(self):
        return random.choice(self.domain)

    def step_in_domain(self, value):
        """
        Find value in the list and then select a neighbor within `self.step` indices away. Assume a circular list.
        """
        EPSILON = 1e-4
        for i in range(len(self.domain)):
            if abs(self.domain[i] - value) < EPSILON:
                new_i = i
                while new_i == i:
                    new_i = i + random.randint(-self.step, self.step)
                return self.domain[new_i % len(self.domain)]


class GeneRuleContinuous(GeneRule):
    def __init__(self, _max=1.0, _min=-1.0, mutation_step=0.5, round_digits=None, exclude=None, allow_mutation=True):
        super().__init__([], step_size=0, allow_mutation=True)
        if exclude is None:
            self.exclude = []
        else:
            self.exclude = exclude
        self._max = _max
        self._min = _min
        self.round_digits = round_digits
        self._range = self._max - self._min
        self.mutation_step = mutation_step
        self.allow_mutation = allow_mutation

    def fetch(self):
        if self.round_digits is None:
            return self.getRandomFloat()
        return self.getRandomRoundedFloat()

    def step_in_domain(self, value):
        """
        Shift the value of the genome element within the step_size and w.r.t. the _min and _max bounds
        """
        augment = (random.random() * self.mutation_step * 2) - self.mutation_step
        return round(self.clip(value + augment), self.round_digits)

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
