import random
import math
from novel_swarms.sensors.AbstractSensor import AbstractSensor
from novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from novel_swarms.sensors.StaticSensor import StaticSensor
from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.world.simulate import main as simulate
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig, StaticAgentConfig, UnicycleAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
import numpy as np

if __name__ == "__main__":

    DISPERSAL_CONTROLLER = [-2.0, -0.6, -20.0, -0.5]
    AGGREGATION_CONTROLLER = [-17.0, -0.3, 0.0, -2.0]
    AGGREGATION_OTHER = [-17.0, 0.3, 0.0, 2.0]
    CYCLIC_OURS = [5.0, 0.3, 12.0, 0.0]
    SEED = None
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = 10
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 12),
            bias=-4,
            degrees=True,
            false_positive=0.1,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            wall_sensing_range=(BL * 4),
            time_step_between_sensing=2,
        )
    ])

    agent_config_a = UnicycleAgentConfig(
        controller=DISPERSAL_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True,
        body_filled=True,
        body_color=(0, 0, 255)
    )

    agent_config_b = UnicycleAgentConfig(
        controller=CYCLIC_OURS,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True,
        body_filled=True,
        body_color=(255, 0, 0)
    )

    heterogeneous_swarm_config = HeterogeneousSwarmConfig()
    heterogeneous_swarm_config.add_sub_populuation(agent_config_a, 20)
    heterogeneous_swarm_config.add_sub_populuation(agent_config_b, 10)

    behavior = [
    ]

    # Initialize Positions
    init_positions = []
    for i in range(20):
        init_positions.append((100, random.randint(50, 400), random.random() * 2 * math.pi))

    for i in range(10):
        init_positions.append((600, random.randint(250, 400), random.random() * 2 * math.pi))

    world_config = RectangularWorldConfig(
        size=(700, 500),
        n_agents=30,
        seed=SEED,
        behavior=behavior,
        show_walls=True,
        agent_initialization=init_positions,
        agentConfig=heterogeneous_swarm_config,
        padding=15
    )

    simulate(world_config=world_config)