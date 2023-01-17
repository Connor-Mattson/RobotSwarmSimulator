"""
Connor Mattson
University of Utah
January 2023
"""
from novel_swarms.sensors.AbstractSensor import AbstractSensor
from novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from novel_swarms.sensors.StaticSensor import StaticSensor
from novel_swarms.world.simulate import main as simulate
from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import UnicycleAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.world.generation.Maze import Maze
from novel_swarms.world.goals.Goal import AreaGoal
import numpy as np
from novel_swarms.world.obstacles.Wall import Wall

if __name__ == "__main__":

    # Set Data Relative to Body Length (GMU Bots)
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
    N_AGENTS = 5
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14,
            distance=(BL * 2),
            bias=0,
            degrees=True,
            false_positive=0.0,
            false_negative=0.0,
            # Rectangle Representing Environment Boundaries
            walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            wall_sensing_range=(BL * 2),
            time_step_between_sensing=1,
            store_history=False
        )
    ])

    agent_config = UnicycleAgentConfig(
        controller=CUSTOM_CONTROLLER,
        agent_radius=BL / 3,
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
    ]

    r = 10
    pi_slice = (2 * np.pi) / N_AGENTS
    start = [20, 20]
    init_positions = [(0, 0, t * pi_slice) for t in range(0, N_AGENTS)]
    init_positions = [(start[0] + x, start[1] + y, t) for x, y, t in init_positions]

    # Generate a Maze factory given the parameters
    # Maze(World Width, World Height, Num_Cells_Tall, Num_Cells_Wide)
    maze = Maze(WIDTH, HEIGHT, 5, 5, padding=GUI_PADDING)

    # Use the maze object to generate a maze and return the wall objects associated with it
    objects = maze.solve_and_return()
    goals = [AreaGoal(200, 200, 75, 75)]

    EVAL_TIL = None
    world_config = RectangularWorldConfig(
        size=(WIDTH + GUI_PADDING, HEIGHT + GUI_PADDING),
        n_agents=N_AGENTS,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=GUI_PADDING,
        show_walls=True,
        agent_initialization=init_positions,
        stop_at=EVAL_TIL,
        objects=objects,
        goals=goals
    )

    world = simulate(world_config=world_config)