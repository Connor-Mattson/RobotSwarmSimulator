"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

"""
import random
from src.novel_swarms.sensors.AbstractSensor import AbstractSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.StaticSensor import StaticSensor
from src.novel_swarms.gui.connectivityGUI import AgentConnectivityGUI
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
import numpy as np

if __name__ == "__main__":

    # Set Data Relative to Body Length
    BL = 15.1

    # Controllers of the Form: [v_0, w_0, v_1, w_1]
    # v_0, v_1 is forward speed for sensor off/on, respectively
    # w_0, w_1 is turning rate for sensor off/on, respectively
    # Note that in Vega et al. v_0 = v_1
    # CUSTOM_CONTROLLER = [17.5, 0.25, 17.5, -0.25]  # Dispersion
    CUSTOM_CONTROLLER = [12.5, 0.5, 12.5, -0.5]  # Stable Milling
    # CUSTOM_CONTROLLER = [17.5, 1.25, 17.5, -1.25]  # Semi-Stable Milling
    # CUSTOM_CONTROLLER = [2.5, 2.0, 2.5, -2.0]  # Colliding Unstable

    # CUSTOM_CONTROLLER = [4.5, 0.3, -3, 0.4]  # Our Dispersal Gene

    SEED = None
    GUI_PADDING = 15
    N_AGENTS = 9
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 12.5),
            bias=-5,
            degrees=True,
            false_positive=0.1,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            wall_sensing_range=(BL * 6),
            time_step_between_sensing=2,
            store_history=True
        )
    ])

    agent_config = UnicycleAgentConfig(
        controller=CUSTOM_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True,
        stop_on_collide=True
    )

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    r = [random.randint(30, 60) for t in range(0, N_AGENTS)]
    pi_slice = (2 * np.pi) / N_AGENTS
    center = (int(BL * 29.8) / 2, int(BL * 29.8) / 2)
    init_positions = [(r[t]*np.cos(t * pi_slice), r[t]*np.sin(t * pi_slice), t * pi_slice) for t in range(0, N_AGENTS)]
    init_positions = [(center[0] + x, center[1] + y, t) for x, y, t in init_positions]

    TIME_STOP = None
    world_config = RectangularWorldConfig(
        size=(WIDTH + GUI_PADDING, HEIGHT + GUI_PADDING),
        n_agents=N_AGENTS,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=GUI_PADDING,
        show_walls=True,
        agent_initialization=init_positions,
        stop_at=TIME_STOP
    )

    gui = None
    gui = AgentConnectivityGUI(WIDTH, 0, 300, HEIGHT, n=N_AGENTS)
    gui.set_title("Agent Connectivity")

    import matplotlib.pyplot as plot
    world = simulate(world_config=world_config, gui=gui)

    mat = np.zeros((TIME_STOP + 1, N_AGENTS, N_AGENTS))
    for i, agent in enumerate(world.population):
        for j, hist_elem in enumerate(agent.sensors.sensors[0].history):
            if hist_elem >= 0:
                mat[j][i][hist_elem] = 1
    print(mat)

