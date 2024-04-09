"""
DO NOT ALTER THIS FILE.
This file should remain a constant reference to a specific behavior.
Please create your own file for simulating or alter 'demo/simulation/playground.py' instead.
"""
from src.novel_swarms.world.simulate import Simulation
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.gui.abstractGUI import AbstractGUI
import random

def get_rand():
    return (random.random() * 2) - 1

if __name__ == "__main__":

    for i in range(5):
        CYCLIC_PURSUIT_CONTROLLER = [get_rand(), get_rand(), get_rand(), get_rand()]
        SEED = 1

        sensors = SensorSet([
            BinaryLOSSensor(angle=0),
        ])

        agent_config = DiffDriveAgentConfig(
            controller=CYCLIC_PURSUIT_CONTROLLER,
            sensors=sensors,
            seed=None,
            body_filled=True
        )

        behavior = [
            AverageSpeedBehavior(),
            AngularMomentumBehavior(),
            RadialVarianceBehavior(),
            ScatterBehavior(),
            GroupRotationBehavior(),
        ]

        world_config = RectangularWorldConfig(
            size=(500, 500),
            n_agents=12,
            seed=None,
            behavior=behavior,
            agentConfig=agent_config,
            padding=15,
            show_walls=False,
        )

        sim = Simulation(world_config=world_config, save_duration=500, save_every_ith_frame=5, gui=AbstractGUI(), show_gui=True)

        for s in range(1510):
            ret = sim.step()
            if ret is not None:
                break
            if s == 1000:
                sim.record_gif()


