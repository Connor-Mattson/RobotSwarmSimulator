from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.ConvexHull import ConvexHull, InverseConvexHull
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig

if __name__ == "__main__":

    CYCLIC_PURSUIT_CONTROLLER = [0.997247279200574, -0.23837063228493535, 0.9741522015725631, 0.9892832036595993]
    SEED = 1

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=CYCLIC_PURSUIT_CONTROLLER,
        sensors=sensors,
        seed=SEED,
        agent_radius=7
    )

    behavior = [
        ConvexHull(),
        InverseConvexHull(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        collide_walls=True,
        show_walls=True,
    )

    simulate(world_config=world_config)
