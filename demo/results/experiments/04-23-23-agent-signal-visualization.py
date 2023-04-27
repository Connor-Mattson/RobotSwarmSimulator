from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.SensorSignal import SensorSignalBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig

if __name__ == "__main__":

    CYCLIC_PURSUIT_CONTROLLER = [-0.7, 0.3, 1.0, 1.0]
    # CYCLIC_PURSUIT_CONTROLLER = [0.7166, 0.8833, 0.7166, 0.8833]
    SEED = 3

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=CYCLIC_PURSUIT_CONTROLLER,
        sensors=sensors,
        seed=SEED,
        agent_radius=7,
        trace_length=1000
    )

    behavior = [
        SensorSignalBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(regularize=False),
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

    simulate(world_config=world_config, world_key_events=True)
