"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

"""
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
import numpy as np

if __name__ == "__main__":
    a = 0.8
    b = 0.4

    # CUSTOM_GENOME = [-0.7, 0.3, -0.7, 0.3, 1.0, 0.9, 1.0, 0.9, np.pi / 6]  # Cyclic Pursuit - Two Sensor
    # CUSTOM_GENOME = [-0.7, -1.0, 1.0, -1.0, -0.7, -1.0, 1.0, -1.0, np.pi / 6]  # Aggregation - Two Sensor
    # CUSTOM_GENOME = [0.2, 0.7, -0.5, -0.1, 0.2, 0.7, -0.5, -0.1, np.pi / 6]  # Dispersal - Two Sensor
    # CUSTOM_GENOME = [0.8, 1.0, 0.5, 0.6, 0.8, 1.0, 0.5, 0.6, np.pi / 6]  # Milling - Two Sensor
    # CUSTOM_GENOME = [1.0, 0.95, 1.0, 0.95, 1.0, 1.0, 1.0, 1.0, np.pi / 6]  # Wall Following - Two Sensor
    CUSTOM_GENOME = [-0.8, -0.7, 0.2, -0.5, -0.7, -0.9, 0.2, -0.5, np.pi / 6]  # Random
    # # CUSTOM_GENOME = [0.8,  0.9, -0.2,  0.5,  0.2, -0.8,  0.7,  0.9, -0.5, np.pi / 6]
    # CUSTOM_GENOME = [0.8, 0.5, 0.6, -0.5, -0.5, -0.0, -0.2, 0.5, -(np.pi / 3)]  # Nested Cycle
    # CUSTOM_GENOME = [-0.4, 0.8, 0.9, -0.2, 0.6, 1.0, 0.6, -0.0, np.pi / 6]  # Concave Cycle
    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
        GenomeBinarySensor(genome_id=8)
    ])

    agent_config = ConfigurationDefaults.DIFF_DRIVE_AGENT
    agent_config.sensors = sensors
    agent_config.agent_radius = 12
    agent_config.wheel_radius = 1
    agent_config.seed = SEED
    agent_config.controller = CUSTOM_GENOME
    agent_config.body_filled = True

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=18,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15
    )

    simulate(world_config=world_config)
