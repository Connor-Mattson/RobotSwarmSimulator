import pygame
import warnings
from multiprocessing import Pool
from ...gui.abstractGUI import AbstractGUI
from ...world.simulate import main as sim
from ...world.simulate import Simulation, DirectEvaluation
import os


def simulate(world_config, terminate_function, show_gui=False):
    try:
        if show_gui is False:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        world = sim(world_config, show_gui=True, gui=AbstractGUI(), stop_detection=terminate_function, step_size=5, auto_start_gif=100, save_duration=500, save_every_ith_frame=10)
        world.gui = None
        return world
    except Exception as e:
        warnings.WarningMessage("World could not be simulated: " + str(e))
    return None

def simulate_batch(world_config_list, terminate_function, show_gui=False):
    ret = []
    for w in world_config_list:
        ret.append(simulate(w, terminate_function, show_gui=False))
    return ret

def evaluate(world_config, output_config, show_gui=False):
    try:
        if show_gui is False:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        world, output = DirectEvaluation(world_config, show_gui=True, gui=AbstractGUI(), output_capture=output_config).evaluate()
        world.gui = None
        return world, output
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

    def execute(self, world_setup: list, world_stop_condition=None, batched=False):

        if not world_setup:
            raise Exception("No world_setup list provided to execute.")

        ret = []
        if not self.single_step:
            with Pool(self.pool_size) as pool:
                ret = pool.starmap(simulate_batch if batched else simulate, zip(world_setup, [world_stop_condition for _ in world_setup]))
        else:
            for w in world_setup:
                if batched:
                    ret.append(simulate_batch(w, world_stop_condition, show_gui=self.with_gui))
                else:
                    print(w.agentConfig.controller)
                    ret.append(simulate(w, world_stop_condition, show_gui=self.with_gui))
        return ret

    def batch_evaluation(self, world_setup: list, output_config):
        if not world_setup:
            raise Exception("No world_setup list provided to execute.")
        ret = []
        with Pool(self.pool_size) as pool:
            ret = pool.starmap(evaluate, zip(world_setup, [output_config for _ in world_setup]))
        return ret

