"""
DO NOT ALTER THIS FILE.
This file should remain a constant reference to a specific behavior.
Please create your own file for simulating or alter 'demo/simulation/playground.py' instead.
"""
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig

if __name__ == "__main__":

    RANDOM_GENOME = [-0.83, -0.75, 0.27, -0.57]
    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=RANDOM_GENOME,
        sensors=sensors,
        seed=SEED,
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
        n_agents=30,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15
    )

    simulate(world_config=world_config)
