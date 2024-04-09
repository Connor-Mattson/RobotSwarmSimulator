from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
import numpy as np

if __name__ == "__main__":
    # CONTROLLER = [-0.45, -1.0, 1.0, -1.0]
    # CONTROLLER = [-0.7, -1.0, 1.0, -1.0]
    # CONTROLLER = [1.0, 0.91, 0.5, 0.48]
    # CONTROLLER = [0.7, 0.9, 0.4, 0.5]
    # CONTROLLER = [-0.83, -0.75, 0.27, -0.57] # Random

    # CONTROLLER = [-0.07, 0.03, 0.05, 0.05]  # Slow Example
    # CONTROLLER = [0.8, 0.9, -0.8, -0.9]  # Passive Example
    # CONTROLLER = [0.2, 0.9, 0.2, 0.9]  # Non-Cooporative Example
    SEED = 25

    # CONTROLLER = [0.8, 0.5, 0.6, -0.5, -0.5, 0.0, -0.2, 0.5, -np.pi / 3]  # Nested Cycles
    CONTROLLER = [-0.4, 0.8, 0.9, -0.1, 0.6, 1.0, 0.9, 0.0, np.pi / 6]  # Concave Path

    # sensors = SensorSet([
    #     BinaryLOSSensor(angle=0, width=3, draw=False),
    # ])

    sensors = SensorSet([
        BinaryLOSSensor(angle=0, width=3, draw=True),
        GenomeBinarySensor(genome_id=8),
    ])

    agent_config = DiffDriveAgentConfig(
        agent_radius=7,
        controller=CONTROLLER,
        sensors=sensors,
        seed=SEED,
        trace_length=160,
        body_color=(100,100,100),
        body_filled=True,
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
        n_agents=24,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        background_color=(255, 255, 255)
    )

    simulate(world_config=world_config, save_duration=2400, save_time_per_frame=40)
