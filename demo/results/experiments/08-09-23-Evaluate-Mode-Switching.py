"""
Example Script
The SwarmSimulator allows control of the world and agents at every step within the main loop
"""
import math
import random
import numpy as np
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation

# Import Agent embodiments
from src.novel_swarms.config.AgentConfig import *
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.agent.MazeAgent import MazeAgent

# Import FOV binary sensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor

# Import Rectangular World Data, Starting Region, and Goal Region
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.world.goals.Goal import CylinderGoal
from src.novel_swarms.world.initialization.RandomInit import RectRandomInitialization

# Import a world subscriber, that can read/write to the world data at runtime
from src.novel_swarms.world.subscribers.WorldSubscriber import WorldSubscriber

# Import the simulation loop
from src.novel_swarms.world.simulate import main as simulator

# Import the Behavior Measurements (Metrics) that can measure the agents over time
from src.novel_swarms.behavior import *

from src.novel_swarms.optim.CMAES import CMAES

# Import the custom Controller Class
from src.novel_swarms.agent.control.Controller import Controller

# ALL UNITS SHOULD BE DEFINED IN TERMS OF AGENT BODY LENGTHS (Agent Diameter).
# Allows for Dynamically Changing the Size of the window

AGENT_BL = 1.0  # This should always be 1 if the above rule is observed.
WORLD_H = 100.0  # Height of World in Body Lengths
WORLD_W = 100.0  # Width of World in Body Lengths
MAX_FORWARD_SPEED = 1.0  # Maximum Forward Speed in Body Lengths / Second
MIN_FORWARD_SPEED = 0.0  # Minimum Forward Speed in Body Lengths / Second
MAX_TURNING_RATE = 1.5  # Maximum Turning Rate in Rad / Second
MIN_TURNING_RATE = -1.5  # Minimum Turning Rate in Rad / Second

VISION_DISTANCE = 17  # Sensor Vision Distance in Body Lengths
VISION_ANGLE = 0.628319  # Angle of Sensor Vision in Radians
START_REGION_SIZE = (7, 7)  # W, H of Starting Region in Body Lengths, centered in Quadrant III

GOAL_CENTER = (WORLD_W * 0.736, WORLD_H * 0.264)  # X, Y of goal center, in Body_Lengths
GOAL_R = 20  # Distance at which we "count" agents as being in the goal, in Body_lengths

FALSE_POSITIVE_RATE = 0.10  # Rate of Sensor Erroneously Detecting an Agent
FALSE_NEGATIVE_RATE = 0.05  # Rate of Sensor Failing to Detect an Agent

NUM_AGENTS = 13  # Number of Agents to Simulate at Anytime.
RATIO_LEVY = 0.5  # Fraction of Population that are Levy Agents

DT = 0.13  # Timestep in Seconds (Sensors, collisions, etc. are evaluated every DT seconds)

SEED = 1  # Seeding for initial Starting positions, FP/FN Readings.

MAX_ALLOWED_STEPS = 3000  # Maximum Steps allowed during simulation


def b2p(x: float):
    """
    (Helper Func) Convert a measurement (param: x), given in Body Lengths, to the appropriate quantity in pixels
    """
    PIXELS_PER_BL = 10
    return x * PIXELS_PER_BL


def milling_controller(agent: MazeAgent):
    """
    An example of a "from scratch" controller that you can code with any information contained within the agent class
    """
    sigma = agent.goal_seen  # Whether the goal has been detected previously by this agent
    gamma = agent.agent_in_sight is not None  # Whether the agent detects another agent

    u_1, u_2 = 0.0, 0.0  # Set these by default
    if not sigma:
        if not gamma:
            u_1, u_2 = b2p(1.0), np.radians(15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
        else:
            u_1, u_2 = b2p(1.0), np.radians(-15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    else:
        u_1, u_2 = 0.0, 0.0  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    return u_1, u_2


def aggregation_controller(agent: MazeAgent):
    sigma = agent.goal_seen  # Whether the goal has been detected previously by this agent
    gamma = agent.agent_in_sight is not None  # Whether the agent detects another agent

    u_1, u_2 = 0.0, 0.0  # Set these by default
    if not sigma:
        if not gamma:
            u_1, u_2 = b2p(0.2), np.radians(15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
        else:
            u_1, u_2 = b2p(1.0), np.radians(15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    else:
        u_1, u_2 = 0.0, 0.0  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    return u_1, u_2


def dispersal_controller(agent: MazeAgent):
    sigma = agent.goal_seen  # Whether the goal has been detected previously by this agent
    gamma = agent.agent_in_sight is not None  # Whether the agent detects another agent

    u_1, u_2 = 0.0, 0.0  # Set these by default
    if not sigma:
        if not gamma:
            u_1, u_2 = b2p(1.0), np.radians(15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
        else:
            u_1, u_2 = b2p(0.1), np.radians(15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    else:
        u_1, u_2 = 0.0, 0.0  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    return u_1, u_2

def wall_following_agent(agent: MazeAgent):
    sigma = agent.goal_seen  # Whether the goal has been detected previously by this agent
    gamma = agent.agent_in_sight is not None  # Whether the agent detects another agent

    u_1, u_2 = 0.0, 0.0  # Set these by default
    if not sigma:
        if not gamma:
            u_1, u_2 = b2p(1.0), np.radians(1)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
        else:
            u_1, u_2 = b2p(1.0), np.radians(0)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    else:
        u_1, u_2 = 0.0, 0.0  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    return u_1, u_2

def configure_robots(controller=None, ratio=0.5, levy_turning_rate=0.2):
    """
    Select the Robot's Sensors and Embodiment, return the robot configuration
    """
    sensors = SensorSet(
        sensors=[
            BinaryFOVSensor(
                theta=VISION_ANGLE / 2,
                # Vision Angle (theta) is defined reflectively across the forward axis, so take total angle / 2.
                degrees=False,  # Indicate that the fov is defined in radians, not degrees
                distance=b2p(VISION_DISTANCE),  # Detection Distance, in pixels
                show=True,  # Whether to show the sensor in the simulator
                goal_sensing_range=b2p(VISION_DISTANCE),  # Goal Detection Distance
                detect_goal_with_added_state=True,
                false_negative=FALSE_NEGATIVE_RATE,
                false_positive=FALSE_POSITIVE_RATE,
            ),
        ],
        custom_state_decision="Linear"
    )

    goal_seeking_robot = MazeAgentConfig(
        sensors=sensors,  # Attach the previously defined sensors to the agent
        # Here, the controller is of the form [v_0, omega_0, v_1, omega_1, ...]
        # controller=[1.5, 0.5, 1.5, -0.5],  # Assign a homogeneous controller to the agents (This can be changed at runtime)
        controller=None,
        # Pass the custom_controller() method (above) to a Controller class for more custom control
        agent_radius=b2p(AGENT_BL / 2),  # Body radius, in pixels
        stop_at_goal=False,  # Don't automatically stop this robot when within goal region
        dt=DT,  # Timestep value
        body_color=(255, 0, 0),  # Set the body color to red
        body_filled=True  # Color in the body,
    )

    aggregation_agent = MazeAgentConfig.from_dict(goal_seeking_robot.as_dict())
    aggregation_agent.controller = Controller(aggregation_controller)
    aggregation_agent.body_color = (255, 0, 0)

    dispersal_agent = MazeAgentConfig.from_dict(goal_seeking_robot.as_dict())
    dispersal_agent.controller = Controller(dispersal_controller)
    dispersal_agent.body_color = (0, 255, 0)

    milling_agent = MazeAgentConfig.from_dict(goal_seeking_robot.as_dict())
    milling_agent.controller = Controller(milling_controller)
    milling_agent.body_color = (0, 0, 255)

    wall_f_agent = MazeAgentConfig.from_dict(goal_seeking_robot.as_dict())
    wall_f_agent.controller = Controller(wall_following_agent)
    wall_f_agent.body_color = (0, 255, 255)

    levy_robot = LevyAgentConfig(
        config=goal_seeking_robot,  # Copy most of the config from the robot above
        levy_constant=0.6,
        forward_rate=b2p(MAX_FORWARD_SPEED),
        turning_rate=levy_turning_rate,
        body_color=(255, 255, 0),  # Set the body color to yellow
        body_filled=True,
        stop_at_goal=False,  # Don't stop when the agent is in the goal region...
        stop_on_goal_detect=True,  # ...stop when the agent DETECTS the goal
        curve_based=True  # Indicate that agents should turn while moving forward, rather than just turn in-place
    )

    # switch_1 = ModeSwitchingAgentConfig(
    #     configs=[aggregation_agent, levy_robot]
    # )
    #
    # switch_2 = ModeSwitchingAgentConfig(
    #     configs=[aggregation_agent, milling_agent]
    # )

    switch_1 = ModeSwitchingAgentConfig(
        configs=[aggregation_agent, dispersal_agent, levy_robot]
    )

    switch_2 = ModeSwitchingAgentConfig(
        configs=[aggregation_agent, milling_agent, milling_agent]
    )

    # switch_1 = ModeSwitchingAgentConfig(
    #     configs=[levy_robot, wall_f_agent]
    # )
    #
    # switch_2 = ModeSwitchingAgentConfig(
    #     configs=[levy_robot, wall_f_agent]
    # )

    # Create a Heterogeneous Swarm and add both agent types to it. Ratio of the subpopulations is determined by the value of RATIO_LEVY
    heterogeneous_swarm = HeterogeneousSwarmConfig()
    heterogeneous_swarm.add_sub_populuation(switch_1, count=(NUM_AGENTS - int(ratio * NUM_AGENTS)))
    heterogeneous_swarm.add_sub_populuation(switch_2, count=int(ratio * NUM_AGENTS))

    return heterogeneous_swarm


def establish_metrics():
    return [PercentageAtGoal(((i + 1) / NUM_AGENTS) - 0.001) for i in range(NUM_AGENTS)]


def configure_env(robot_config, size=(500, 500), num_agents=20, _hash=None, seed=None, stop_at=None):
    """
    Select the World for the robots to interact in. Define the start region and goal region.

    Params:
    - robot_config: A robot configuration model (see configure_robots func)
    - size (optional, default: (500, 500)): A two-element tuple containing the WIDTH, HEIGHT of the world, in pixels
    - num_agents (optional, default: 20): The number of agents to instantiate in the environment

    Return: The World Configuration Data
    """

    # Randomly Assign Agents to an x, y, $/theta$ orientation within the specified bounding box
    bb_center = (size[0] * 0.25, size[1] * 0.75)
    shift_x, shift_y = b2p(START_REGION_SIZE[0] / 2), b2p(START_REGION_SIZE[1] / 2)
    bb_upper_left = (bb_center[0] - shift_x, bb_center[1] - shift_y)
    bb_bottom_right = (bb_center[0] + shift_x, bb_center[1] + shift_y)
    starting_region = RectRandomInitialization(
        num_agents=num_agents,
        bb=(bb_upper_left, bb_bottom_right),  # Spawn Bounding Box
        seed=seed
    )

    # Create a Goal for the Agents to find
    goal_region = CylinderGoal(
        x=b2p(GOAL_CENTER[0]),  # Center X, in pixels
        y=b2p(GOAL_CENTER[1]),  # Center y, in pixels
        r=b2p(0.5),  # Radius of physical cylinder object
        range=b2p(GOAL_R)  # Range, in pixels, at which agents are "counted" as being at the goal
    )

    # Create the World for the Agents to interact in
    env = RectangularWorldConfig(
        size=size,
        agentConfig=robot_config,
        n_agents=num_agents,
        behavior=establish_metrics(),  # Attach our desired measurements to the world
        seed=seed,
        init_type=starting_region,  # A starting region where agents will spawn at t=0
        goals=[goal_region],  # A list of goals for the robots to find
        collide_walls=True,  # Use No Environment Walls for this problem
        show_walls=True,  # Hide Default Walls,
        metadata={'hash': _hash},
        stop_at=stop_at,
        padding=15
    )

    return env


def get_evolution_worlds():
    worlds = []
    seeds = [i for i in range(500)]
    for seed in seeds:
        robo_config = configure_robots(controller=[0 for _ in range(6)], levy_turning_rate=float(np.radians(15)), ratio=1.0)
        # np.random.seed(seed)
        # random.seed(seed)
        world_config = configure_env(robo_config, num_agents=NUM_AGENTS, stop_at=MAX_ALLOWED_STEPS, seed=seed, size=(b2p(WORLD_W), b2p(WORLD_H)))
        worlds.append(world_config)
    return worlds


def test_world():
    robot_conf = configure_robots()
    world_conf = configure_env(robot_config=robot_conf, num_agents=NUM_AGENTS, size=(b2p(WORLD_W), b2p(WORLD_H)))

    # print(robot_config)

    simulator(
        world_config=world_conf,
        world_key_events=True
    )

if __name__ == "__main__":
    test_world()
