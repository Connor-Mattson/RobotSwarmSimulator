"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.
"""
from src.novel_swarms.sensors.AbstractSensor import AbstractSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.StaticSensor import StaticSensor
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
import numpy as np
import math

if __name__ == "__main__":
    # a = 0.8
    # b = 0.4

    # [vl_0, vr_0, vl_1, vr_1]
    # CUSTOM_GENOME = [-0.7, -1.0, 1.0, -1.0]  # Aggregation
    # CUSTOM_GENOME = [-0.7, 0.3, 1.0, 1.0]  # Cyclic Pursuit
    # CUSTOM_GENOME = [0.2, 0.7, -0.5, -0.1]  # Dispersal
    # CUSTOM_GENOME = [0.8, 1.0, 0.5, 0.6]  # Milling
    # CUSTOM_GENOME = [1.0, 0.95, 1.0, 1.0]  # Wall Following
    # CUSTOM_GENOME = [-0.8, -0.7, 0.2, -0.5]  # Random
    CUSTOM_GENOME = [0.5118773770184124, 0.12775717006510645, 0.2612236621699462, 0.5507791161133743]

    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0, draw=True),
    ])

    # agent_config = DiffDriveAgentConfig(
    #     controller=CUSTOM_GENOME,
    #     agent_radius=5,
    #     dt=1.0,
    #     wheel_radius=2,
    #     sensors=sensors,
    #     seed=None,
    # )

    agent_config = DiffDriveAgentConfig(
        controller=CUSTOM_GENOME,
        sensors=sensors,
        trace_length=0,
        agent_radius=7,
        # wheel_radius=1,
        # body_color="Random",
        body_filled=True,
    )

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
        TotalCollisionsBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=18,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        stop_at=None,
    )

    simulate(world_config=world_config)
