"""
DO NOT ALTER THIS FILE.
This file should remain a constant reference to a specific behavior.
Please create your own file for simulating or alter 'demo/simulation/playground.py' instead.

Connor Mattson
University of Utah
September 2022
"""
from src.world.simulate import main as simulate
from src.behavior.AngularMomentum import AngularMomentumBehavior
from src.behavior.AverageSpeed import AverageSpeedBehavior
from src.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.behavior.RadialVariance import RadialVarianceBehavior
from src.behavior.ScatterBehavior import ScatterBehavior
from src.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.sensors.SensorSet import SensorSet
from src.config.AgentConfig import DiffDriveAgentConfig
from src.config.WorldConfig import RectangularWorldConfig

if __name__ == "__main__":

    RANDOM_GENOME = [-0.83889, -0.7501, 0.27992, -0.57196]
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
