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
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig, StaticAgentConfig, UnicycleAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
import numpy as np

if __name__ == "__main__":

    MILLING_CONTROLLER = [12.5, 0.5, 12.5, -0.5]
    SEED = None
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = 10
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 16),
            bias=-4,
            degrees=True,
            false_positive=0.1,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            wall_sensing_range=(BL * 0),
            time_step_between_sensing=2,
        )
    ])

    agent_config_a = UnicycleAgentConfig(
        controller=MILLING_CONTROLLER,
        agent_radius=BL,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True
    )

    agent_config_b = StaticAgentConfig(agent_radius=BL)

    heterogeneous_swarm_config = HeterogeneousSwarmConfig()
    heterogeneous_swarm_config.add_sub_populuation(agent_config_a, 8)
    heterogeneous_swarm_config.add_sub_populuation(agent_config_b, 0)

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=30,
        seed=SEED,
        behavior=behavior,
        show_walls=True,
        agentConfig=heterogeneous_swarm_config,
        padding=15
    )

    simulate(world_config=world_config)