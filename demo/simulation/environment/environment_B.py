from src.novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal, PercentageAtGoal
from src.novel_swarms.sensors.AbstractSensor import AbstractSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.StaticSensor import StaticSensor
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import MazeAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.world.generation.Maze import Maze
from src.novel_swarms.world.goals.Goal import AreaGoal
import numpy as np
from src.novel_swarms.world.obstacles.Wall import Wall

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

    SEED = 1
    GUI_PADDING = 15
    N_AGENTS = 10
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14,
            distance=(BL * 8),
            bias=0,
            degrees=True,
            false_positive=0.10,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            wall_sensing_range=(BL * 3),
            time_step_between_sensing=1,
            store_history=False
        )
    ])

    agent_config = MazeAgentConfig(
        controller=CUSTOM_CONTROLLER,
        agent_radius=BL / 3,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=False
    )

    behavior = [
        DistanceToGoal(),
        AgentsAtGoal(),
        PercentageAtGoal(0.01),
        PercentageAtGoal(0.10),
        PercentageAtGoal(0.25),
        PercentageAtGoal(0.50),
        PercentageAtGoal(0.80),
        PercentageAtGoal(1.0),
    ]

    r = 10
    pi_slice = (2 * np.pi) / N_AGENTS
    start = [20, 20]
    init_positions = [(0, 0, t * pi_slice) for t in range(0, N_AGENTS)]
    init_positions = [(start[0] + x, start[1] + y, t) for x, y, t in init_positions]

    # Original Example
    # objects = [
    #     Wall(None, 104, 104, 2, 400),
    #     Wall(None, 193, 104, 2, 400),
    #     Wall(None, 282, 104, 2, 400),
    #     Wall(None, 371, 104, 2, 400),
    # ]

    # Tricky Maze
    objects = [
        Wall(None, 180, 193, 120, 5),
        Wall(None, 180, 193, 5, 91),
        Wall(None, 300, 193, 5, 91),
        Wall(None, 238, 350, 5, 100),
        Wall(None, 236, 348, 10, 5),
    ]

    # Use the maze object to generate a maze and return the wall objects associated with it
    # Generate a Maze factory given the parameters
    # Maze(World Width, World Height, Num_Cells_Tall, Num_Cells_Wide)

    # maze = Maze(WIDTH, HEIGHT, 5, 5, padding=GUI_PADDING)
    # objects = maze.solve_and_return()
    # for o in objects:
    #     print(repr(o))

    # Add Goal
    # goals = []
    goals = [AreaGoal(200, 200, 75, 20)]

    EVAL_TIL = None
    world_config = RectangularWorldConfig(
        size=(WIDTH + GUI_PADDING, HEIGHT + GUI_PADDING),
        n_agents=N_AGENTS,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=GUI_PADDING,
        show_walls=True,
        collide_walls=True,
        agent_initialization=None,
        stop_at=EVAL_TIL,
        objects=objects,
        goals=goals
    )

    world = simulate(world_config=world_config)