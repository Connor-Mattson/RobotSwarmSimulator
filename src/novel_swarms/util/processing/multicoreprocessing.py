import warnings
from multiprocessing import Pool
from novel_swarms.world.simulate import main as sim


def simulate(world_config, terminate_function, show_gui=False):
    try:
        world = sim(world_config, show_gui=show_gui, stop_detection=terminate_function, step_size=5)
        return world
    except Exception as e:
        warnings.WarningMessage("World could not be simulated: " + str(e))
    return None

class MultiWorldSimulation:
    """
    A Multi-Threaded Implementation of the novel_swarms.world.simulate package
    """

    def __init__(self, pool_size=4, single_step=False, with_gui=False):
        self.single_step = single_step
        self.with_gui = with_gui
        self.pool_size = pool_size

    def execute(self, world_setup: list, world_stop_condition=None):

        if not world_setup:
            raise Exception("No world_setup list provided to execute.")

        ret = []
        if not self.single_step:
            with Pool(self.pool_size) as pool:
                ret = pool.starmap(simulate, zip(world_setup, [world_stop_condition for _ in world_setup]))
        else:
            for w in world_setup:
                print(w.agentConfig.controller)
                ret.append(simulate(w, world_stop_condition, show_gui=self.with_gui))

        return ret
