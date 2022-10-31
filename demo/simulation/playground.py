"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from novel_swarms.sensors.AbstractSensor import AbstractSensor
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
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
import numpy as np

if __name__ == "__main__":
    # a = 0.8
    # b = 0.4

    # CUSTOM_GENOME = [-0.7, -1.0, 1.0, -1.0]  # Aggregation
    CUSTOM_GENOME = [-0.7, 0.3, 1.0, 1.0]  # Cyclic Pursuit
    # CUSTOM_GENOME = [0.2, 0.7, -0.5, -0.1]  # Dispersal
    # CUSTOM_GENOME = [-0.69, -0.77, 0.05, -0.4]  # Milling
    # CUSTOM_GENOME = [1.0, 0.98, 1.0, 1.0]  # Wall Following
    # CUSTOM_GENOME = [-0.83, -0.75, 0.27, -0.57]  # Random
    # CUSTOM_GENOME = [0.8346  ,   0.5136 ,    0.87086294, 0.7218    ]
    # CUSTOM_GENOME = [-0.788, 0.7441, 0.9298, -0.4975]
    # CUSTOM_GENOME = [1.0, 0.95, 0.99, 1.0] # Wall-F
    # CUSTOM_GENOME = [-0.942, -0.592, -1.0, -0.132]
    # CUSTOM_GENOME = [0.667, -1.0, 1.0, 0.05]

    SEED = None

    sensors = SensorSet([
        # StaticSensor(),
        BinaryLOSSensor(angle=0),
        # BinaryFOVSensor(theta=14 / 2, distance=300, degrees=True)
    ])

    agent_config = DiffDriveAgentConfig(
        controller=CUSTOM_GENOME,
        agent_radius=5,
        dt=1.0,
        wheel_radius=1,
        sensors=sensors,
        seed=None,
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
        n_agents=10,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=100
    )

    simulate(world_config=world_config)
