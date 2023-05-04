import numpy as np
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.SensorSignal import SensorSignalBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.sensors.RegionalSensor import RegionalSensor
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig, DroneAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.world.goals.GrowthRegion import GrowthRegion

if __name__ == "__main__":

    DRONE_CONTROLLER = [
        # Z Off, Forward Off
        (0.0, -1.0, 0),
        (0.0, -1.0, 0),
        (0.0, -1.0, 0),
        (0.0, -1.0, 0),
        # Z Off, Forward Detected
        (0.0, -1.0, 0),
        (0.0, -1.0, 0),
        (0.0, -1.0, 0),
        (0.0, -1.0, 0),
        # Z On, Forward Off
        (0, 0, 0),  # Left off, Right off
        (1, 0, 0),  # Left off, Right on
        (-1, 0, 0),  # Left on, right off
        (0, 0, 0),  # Left on, right on
        # Z On, Forward On
        (0, 0, np.pi / 16),
        (0, 0, np.pi / 16),
        (0, 0, np.pi / 16),
        (0, 0, np.pi / 16),
    ]
    SEED = None

    sensors = SensorSet([
        RegionalSensor(0),
        BinaryFOVSensor(theta=(np.pi/16), distance=70, bias=0),
        BinaryFOVSensor(theta=(np.pi/16), distance=70, bias=(np.pi / 2)),
        BinaryFOVSensor(theta=(np.pi/16), distance=70, bias=(3 * np.pi / 2)),
    ])

    agent_config = DroneAgentConfig(
        controller=DRONE_CONTROLLER,
        sensors=sensors,
        seed=SEED,
        agent_radius=7,
    )

    behavior = [
        RadialVarianceBehavior(),
        ScatterBehavior(regularize=False),
    ]

    fire_region = GrowthRegion(
        None,
        [[50.0, 50.0], [20.0, 100.0], [200.0, 200.0], [300.0, 400.0], [400.0, 40.0]],
        detectable=False,
        growth_step=0
    )

    init = [((x * 15) + 100, (x * 25) + 500, -np.pi / 2) for x in range(12)]
    # init = [(500, 500)]

    world_config = RectangularWorldConfig(
        size=(500, 800),
        n_agents=12,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        collide_walls=True,
        show_walls=True,
        agent_initialization=init,
        objects=[fire_region]
    )


    def grow_fire(world):
        if world.total_steps % 20 == 0:
            world.objects[0].step()


    simulate(world_config=world_config, world_key_events=False, stop_detection=grow_fire)
