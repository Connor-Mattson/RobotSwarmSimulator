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

    CUSTOM_GENOME = [0.8, 0.5, 0.6, -0.5, -0.5, -0.0, -0.2, 0.5, -(np.pi / 3)]
    SEED = 9

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
        GenomeBinarySensor(genome_id=8)
    ])

    agent_config = ConfigurationDefaults.DIFF_DRIVE_AGENT
    agent_config.sensors = sensors
    agent_config.seed = SEED
    agent_config.controller = CUSTOM_GENOME
    agent_config.agent_radius = 5
    agent_config.wheel_radius = 2

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15
    )

    simulate(world_config=world_config)
