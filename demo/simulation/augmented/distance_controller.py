"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

"""
from src.novel_swarms.behavior.Centroid import Centroid
from src.novel_swarms.sensors.AbstractSensor import AbstractSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.StaticSensor import StaticSensor
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior import *
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.DiscreteDistanceFOVSensor import DiscreteDistanceFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import UnicycleAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.behavior.AlgebraicConnectivity import AlgebraicConn
import numpy as np

if __name__ == "__main__":

    # Set Data Relative to Body Length
    BL = 15.1

    #### BIN_THRESHOLD = [0.5, 1.0]
    # Lattice Formation
    # CUSTOM_CONTROLLER = [-0.793, -1.25,  -3.67,  -0.221,  1.49,  -1.788]
    # CUSTOM_CONTROLLER = [4.747,  1.437, -4.684,  1.456,  9.184,  1.475]

    # "Pecking"
    # CUSTOM_CONTROLLER = [6.154616, 1.908, -8.153, 1.79539, 5.700, -1.13]
    # CUSTOM_CONTROLLER = [-5.96,  -1.434, -5.638,  1.99,   8.843, -1.134]

    # Circle with custom r
    # CUSTOM_CONTROLLER = [4.867, -1.8,   -7.451,  0.554,  4.105,  0.07]

    # Multi-Aggregate
    CUSTOM_CONTROLLER = [2.44, -1.302, 7.011, -1.698, -2.719, -0.296, -9.935, -0.066]

    #### BIN_THRESHOLD = [0.33, 0.66, 1.0]
    # CUSTOM_CONTROLLER = [4.747, 1.437, -4.684, 1.456, 9.184, 1.475, 1.0, 1.0]

    SEED = 1
    GUI_PADDING = 15
    N_AGENTS = 7
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
            DiscreteDistanceFOVSensor(
                theta=14 / 2,
                distance=(BL * 8.0),
                bin_thresholds=[0.5, 1.0],
                bias=0,
                degrees=True,
                false_positive=0.0,
                false_negative=0.0,
                time_step_between_sensing=1,
                store_history=True
            )
        ],
        custom_state_decision="Linear",
    )

    agent_config = UnicycleAgentConfig(
        controller=CUSTOM_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=False
    )

    behavior = [
        ScatterBehavior(history=1, regularize=False),
        Centroid(),
        # AlgebraicConn(),
    ]

    r = 60
    pi_slice = (2 * np.pi) / N_AGENTS
    center = (int(BL * 29.8) / 2, int(BL * 29.8) / 2)
    init_positions = [(r*np.cos(t * pi_slice), r*np.sin(t * pi_slice), t * pi_slice) for t in range(0, N_AGENTS)]
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
        show_walls=True,
        agent_initialization=init_positions,
        stop_at=EVAL_TIL,
    )

    # import matplotlib.pyplot as plot
    world = simulate(world_config=world_config)

    # for i in range(100):
    #     c = [
    #         ((2 * np.random.random()) - 1) * (10 if j % 2 == 0 else 2) for j in range(8)
    #     ]
    #     print((np.round(np.array(c), 3).tolist()))
    #     agent_config.controller = c
    #     world_config.agentConfig = agent_config
    #     world = simulate(world_config=world_config)


