from multiprocessing import Pool
from novel_swarms.world.simulate import main as sim


def simulate(world_config):
    world = sim(world_config, show_gui=False)
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
            ret = pool.map(simulate, world_setup)
        return ret
