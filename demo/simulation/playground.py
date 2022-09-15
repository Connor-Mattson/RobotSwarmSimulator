"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

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

    CUSTOM_GENOME = [0.0, 0.0, 0.0, 0.0]
    SEED = None

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=CUSTOM_GENOME,
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
