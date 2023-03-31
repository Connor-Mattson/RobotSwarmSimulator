from multiprocessing import Pool
from novel_swarms.world.simulate import main as sim


def simulate(world_config, terminate_function):
    world = sim(world_config, show_gui=False, stop_detection=terminate_function)
    return world

class MultiWorldSimulation:
    """
    A Multi-Threaded Implementation of the novel_swarms.world.simulate package
    """

    def __init__(self, pool_size=4):
        self.pool_size = pool_size

    def execute(self, world_setup: list, world_stop_condition=None):

        if not world_setup:
            raise Exception("No world_setup list provided to execute.")

        ret = []
        with Pool(self.pool_size) as pool:
            ret = pool.starmap(simulate, zip(world_setup, [world_stop_condition for _ in world_setup]))
        return ret
