from src.novel_swarms.world.initialization.AbstractInit import AbstractInitialization
from src.novel_swarms.world.World import World
import numpy as np
from typing import Tuple, Iterable

class RectRandomInitialization(AbstractInitialization):
    """
    RandomInitialization: A random initialization of the agents in the environment.
    """
    def __init__(self, num_agents: int, bb:Tuple[Tuple, Tuple]=None, seed=None):
        """
        Initialize the RandomInitialization Class
        @params
        num_agents: The number of agents present in the simulation (int, required)
        bb: A Bounding box of the form ((x1, y1), (x2, y2)), where x1 and y1 are the Upper Left corner and 
            x2, y2 are the Bottom Right corner.
        """
        super().__init__()
        self.num_agents = num_agents
        self.bb = bb
        self.seed = seed

        if self.seed is not None:
            np.random.seed(self.seed)

        # Store the initialization information in an iterable
        self.positions = []

        # Determine Positions, but don't set them until the user explicitly calls 'set_to_world' method
        self._calculate_positions()
        

    def _calculate_positions(self):
        """
        Using the bounding box (self.bb) information, randomly sample positions from the rectangle, and orientations from the range [0, 2pi].
        """
        bounds = [(self.bb[0][0], self.bb[1][0]), (self.bb[0][1], self.bb[1][1]), (0, 2*np.pi)]
        self.positions = self.random_vec(bounds, n=self.num_agents, round_to=2)


    def random_vec(self, bounding_set: Iterable[Tuple], n:int=1, round_to:int=5):
        """
        Retrieve n random vectors bounded between specified values.
        
        @params
        bounding_set: An iterable of Tuples defining both the size (len) of the vector and the upper and lower bounds for each values of the output
        rount_to: An integer (default: 5) indicating the number of decimal places to round the output to.
        n: The number of vectors to randomly retreive (default: 1)
        
        @return
        A vector of size len(bounding_set), containing random values aligned with the ranges defined by the bounds

        @example
        Note: Outputs are NOT deterministic. Examples only.
        
        >>> random_vec(bounding_set=[(-1, 1), (0, 2pi)])
        [-0.24532, 0.53487]

        >>> random_vec(bounding_set=[(0, 1), (0, 1), (0, 10)], n=3, round_to=1)
        [
            [0.3, 0.4, 8.3],
            [0.2, 0.7, 4.1],
            [0.5, 0.5, 9.1]
        ]

        For bounding_set = [(-1, 1), (0, 2pi)], a valid return may be a vector with first element within the range [-1, 1],
          inclusive and second element in the range [0, 2pi], inclusive.
        """

        # Precondition n > 0
        if n <= 0:
            raise Exception(f"The number of vectors requested (n) must be greater than zero, not {n}.")

        # Determine the spread between max and min
        spread = [y - x for x, y in bounding_set]
       
        # Precondition: Check that all second values of the bounds are greater than the first values
        if min(spread) <= 0:
            raise Exception(f"The input bounding_set must be an iterable of tuples of the form (x, y), where y is greater than x for all elements of the bounds vector. Your bounds: {bounding_set}")

        ret = []
        for _ in range(n):
            randoms = np.random.random(size=len(bounding_set))
            vec = []
            for i in range(len(randoms)):
                vec.append(round((randoms[i] * spread[i]) + bounding_set[i][0], ndigits=round_to))
            ret.append(vec)

        # In the special case where rows = 1, just return that row
        if n == 1:
            return ret[0]
        
        # In the special case where cols = 1, return the col as a list.
        if len(bounding_set) == 1:
            return [i[0] for i in ret]

        return ret