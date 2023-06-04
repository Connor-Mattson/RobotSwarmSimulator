"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

"""
from src.novel_swarms.sensors.AbstractSensor import AbstractSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.StaticSensor import StaticSensor
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import UnicycleAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.behavior.AlgebraicConnectivity import AlgebraicConn
import numpy as np

if __name__ == "__main__":

    # Set Data Relative to Body Length
    BL = 15.1

    # Controllers of the Form: [v_0, w_0, v_1, w_1]
    # v_0, v_1 is forward speed for sensor off/on, respectively
    # w_0, w_1 is turning rate for sensor off/on, respectively
    # Note that in Vega et al. v_0 = v_1, w_0 = -w_1

    # CUSTOM_CONTROLLER = [17.5, 0.25, 17.5, -0.25]  # Dispersion
    # CUSTOM_CONTROLLER = [12.5, 0.5, 12.5, -0.5]  # Stable Milling
    # CUSTOM_CONTROLLER = [17.5, 1.25, 17.5, -1.25]  # Semi-Stable Milling
    # CUSTOM_CONTROLLER = [2.5, 2.0, 2.5, -2.0]  # Colliding Unstable
    # CUSTOM_CONTROLLER = [4.5, 0.3, -3, 0.4]  # Our Dispersal Gene

    # forwards = [2.5 * i for i in range(1, 8)]
    # rotation = [0.25 * i for i in range(1, 9)]
    # i, j = 1, 2
    # F_S = forwards[j]
    # T_R = rotation[i]
    # print("x:", T_R, "y:", F_S)
    # CUSTOM_CONTROLLER = [F_S, T_R, F_S, -T_R]

    # Behavior Discovery Genomes
    # CUSTOM_CONTROLLER = [18.0, -0.1, 14.0, 0.5]  # Wall Following
    # CUSTOM_CONTROLLER = [16.6, -0.4, 14.0, 0.5]  # Wall Following - Sweeping Version
    # CUSTOM_CONTROLLER = [-12.0, -0.6, -14.0, -0.5]  # Dispersal
    # CUSTOM_CONTROLLER = [8.0, -0.9, 15.0, 0.1]  # Milling/Cyclic
    # CUSTOM_CONTROLLER = [-1.7, 0.2, 0.0, 0.2]

    CUSTOM_CONTROLLER = [5, 0.5, 0.0, 0.0]

    # CUSTOM_CONTROLLER = [20.0, -1.6, 20.0, 1.2]

    SEED = 1
    GUI_PADDING = 15
    N_AGENTS = 1
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=50 / 2,
            distance=(BL * 12.5),
            # distance=(BL * 3),
            bias=-7,
            degrees=True,
            false_positive=0.0,
            false_negative=0.0,
            # Rectangle Representing Environment Boundaries
            # walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            walls=None,
            wall_sensing_range=(BL * 6),
            time_step_between_sensing=3,
            store_history=True
        )
    ])

    agent_config = UnicycleAgentConfig(
        controller=CUSTOM_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=False
    )

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
        # AlgebraicConn(),
    ]

    r = 80
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
    # neighbors_at = int(input("Time of Neighbor?"))
    # converged_at = int(input("Time of Convergence?"))
    # for i, agent in enumerate(world.population):
    #     print(agent.sensors.sensors[0].history)
    #     f = plot.figure()
    #     f.set_figwidth(18)
    #     f.set_figheight(5)
    #     plot.step([x for x in range(EVAL_TIL + 1)], agent.sensors.sensors[0].history, where='post')
    #     plot.axvline(x=neighbors_at, color='r', linestyle='dashed', label='vline_multiple - full height')
    #     plot.axvline(x=converged_at, color='r', linestyle='dashed', label='vline_multiple - full height')
    #     plot.xlabel("Time (Frames)")
    #     plot.ylabel("Sensor Value")
    #     plot.title(f"Sensor Activity for Agent {i + 1} during Milling Behavior")
    #     plot.show()
