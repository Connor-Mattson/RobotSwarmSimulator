"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from novel_swarms.sensors.AbstractSensor import AbstractSensor
from novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from novel_swarms.sensors.StaticSensor import StaticSensor
from novel_swarms.world.simulate import main as simulate
from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import UnicycleAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
import numpy as np

if __name__ == "__main__":

    # Set Data Relative to Body Length
    BL = 15.1

    # Controllers of the Form: [v_0, w_0, v_1, w_1]
    # v_0, v_1 is forward speed for sensor off/on, respectively
    # w_0, w_1 is turning rate for sensor off/on, respectively
    # Note that in Vega et al. v_0 = v_1
    # CUSTOM_GENOME = [17.5, 0.25, 17.5, -0.25]  # Dispersion
    # CUSTOM_GENOME = [15, 0.75, 15, -0.75]  # Stable Milling
    CUSTOM_GENOME = [7.5, 1.0, 7.5, -1.0]  # Semi-Stable Milling
    # CUSTOM_GENOME = [2.5, 2.0, 2.5, -2.0]  # Colliding Unstable

    SEED = None

    sensors = SensorSet([
        BinaryFOVSensor(theta=14 / 2, distance=(BL * 13.25), bias=-10, degrees=True, false_positive=0.1, false_negative=0.05)
    ])

    agent_config = UnicycleAgentConfig(
        controller=CUSTOM_GENOME,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True
    )

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    GUI_PADDING = 15
    world_config = RectangularWorldConfig(
        size=(int(BL * 29.8) + GUI_PADDING, int(BL * 29.8) + GUI_PADDING),
        n_agents=9,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=GUI_PADDING,
        show_walls=True
    )

    simulate(world_config=world_config)
