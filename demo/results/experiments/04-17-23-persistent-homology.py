from novel_swarms.behavior.PersistentHomology import PersistentHomology
from novel_swarms.world.simulate import main as simulate
from novel_swarms.behavior.ConvexHull import ConvexHull, InverseConvexHull
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig

if __name__ == "__main__":
    CYCLIC_PURSUIT_CONTROLLER = [0.7, 0.3, 1.0, 1.0]
    SEED = None

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
        PersistentHomology(dims=0, history_size=10, max_death=True),
        PersistentHomology(dims=1, history_size=10, draw_cycles=True, max_death=True)
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=15,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        collide_walls=True,
        show_walls=True,
    )

    simulate(world_config=world_config)