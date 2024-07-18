"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

"""
from src.novel_swarms.behavior.Centroid import Centroid
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.sensors.AbstractSensor import AbstractSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.StaticSensor import StaticSensor
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior import *
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import MechanumAgentConfig
from src.novel_swarms.world.initialization.RandomInit import RectRandomInitialization
from src.novel_swarms.behavior.AlgebraicConnectivity import AlgebraicConn
import numpy as np

def rand():
    return np.round((np.random.rand() * 2) - 1, 2)

if __name__ == "__main__":

    # Set Data Relative to Body Length
    BL = 10  # (Inches)

    # Controllers of the Form [u1_off, u2_off, u3_off, u4_off, u1_on, u2_on, u3_on, u4_on]
    # CUSTOM_CONTROLLER = [9.2835, -1.3957, -0.0551, -0.7047,  3.9494,  0.4763]
    CUSTOM_CONTROLLER = [rand() for _ in range(6)]
    # print(CUSTOM_CONTROLLER)

    SEED = 1
    GUI_PADDING = 15
    N_AGENTS = 2
    WIDTH, HEIGHT = int(BL * 50), int(BL * 50)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=52 / 2,
            distance=(BL * 5.7142),
            # distance=(BL * 3),
            degrees=True,
            false_positive=0.0,
            false_negative=0.0,
            # Rectangle Representing Environment Boundaries
            # walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            walls=None,
            # wall_sensing_range=(BL * 6),
            # time_step_between_sensing=1,
            # store_history=True
            show=True,
        )
    ])

    agent_config = MechanumAgentConfig(
        controller=CUSTOM_CONTROLLER,
        lx=(BL) / 2,
        ly=(BL * 0.9142) / 2,
        wheel_radius=BL * 0.57,
        dt=0.13,
        sensors=sensors,
        seed=None,
        idiosyncrasies=False
    )

    behavior = [
        ScatterBehavior(history=1, regularize=True),
        # Centroid(),
        # AlgebraicConn(),
    ]

    r = 100
    pi_slice = (2 * np.pi) / N_AGENTS
    center = (int(WIDTH) / 2, int(HEIGHT) / 2)
    init_positions = [(r*np.cos(t * pi_slice), r*np.sin(t * pi_slice), 0) for t in range(0, N_AGENTS)]
    init_positions = [(center[0] + x, center[1] + y, t) for x, y, t in init_positions]

    EVAL_TIL = None
    world_config = RectangularWorldConfig(
        size=(WIDTH + GUI_PADDING, HEIGHT + GUI_PADDING),
        n_agents=N_AGENTS,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=GUI_PADDING,
        collide_walls=False,
        show_walls=False,
        # init_type=None,
        init_type=RectRandomInitialization(num_agents=N_AGENTS, bb=((200, 200), (300, 300))),
        # agent_initialization=init_positions,
        stop_at=EVAL_TIL,
    )

    world = simulate(world_config=world_config)
