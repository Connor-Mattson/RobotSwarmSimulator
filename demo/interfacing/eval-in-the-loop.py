"""
Example Script
The SwarmSimulator allows control of the world and agents at every step within the main loop
"""
import math
import random
import numpy as np

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

# Import the custom Controller Class
from src.novel_swarms.agent.control.Controller import Controller


# ALL UNITS SHOULD BE DEFINED IN TERMS OF AGENT BODY LENGTHS (Agent Diameter).
# Allows for Dynamically Changing the Size of the window

AGENT_BL = 1.0  # This should always be 1 if the above rule is observed.
WORLD_H = 132.0  # Height of World in Body Lengths
WORLD_W = 132.0  # Width of World in Body Lengths
MAX_FORWARD_SPEED = 1.0  # Maximum Forward Speed in Body Lengths / Second
MIN_FORWARD_SPEED = 0.0  # Minimum Forward Speed in Body Lengths / Second
MAX_TURNING_RATE = 1.5   # Maximum Turning Rate in Rad / Second
MIN_TURNING_RATE = -1.5  # Minimum Turning Rate in Rad / Second

VISION_DISTANCE = 17  # Sensor Vision Distance in Body Lengths
VISION_ANGLE = 0.628319  # Angle of Sensor Vision in Radians
START_REGION_SIZE = (20, 20)  # W, H of Starting Region in Body Lengths, centered in Quadrant III

GOAL_CENTER = (WORLD_W * 0.75, WORLD_H * 0.25)  # X, Y of goal center, in Body_Lengths
GOAL_R = 20  # Distance at which we "count" agents as being in the goal, in Body_lengths

FALSE_POSITIVE_RATE = 0.10  # Rate of Sensor Erroneously Detecting an Agent
FALSE_NEGATIVE_RATE = 0.05  # Rate of Sensor Failing to Detect an Agent

NUM_AGENTS = 20  # Number of Agents to Simulate at Anytime.
RATIO_LEVY = 0.2  # Fraction of Population that are Levy Agents

DT = 0.13  # Timestep in Seconds (Sensors, collisions, etc. are evaluated every DT seconds)

SEED = 1  # Seeding for initial Starting positions, FP/FN Readings.

def b2p(x: float):
    """
    (Helper Func) Convert a measurement (param: x), given in Body Lengths, to the appropriate quantity in pixels
    """
    PIXELS_PER_BL = 7
    return x * PIXELS_PER_BL

def custom_controller(agent: MazeAgent):
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

def configure_robots():
    """
    Select the Robot's Sensors and Embodiment, return the robot configuration
    """
    sensors = SensorSet(
        sensors=[
            BinaryFOVSensor(
                theta=VISION_ANGLE / 2,  # Vision Angle (theta) is defined reflectively across the forward axis, so take total angle / 2.
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
        controller=Controller(custom_controller),  # Pass the custom_controller() method (above) to a Controller class for more custom control
        agent_radius=b2p(AGENT_BL / 2),  # Body radius, in pixels
        stop_at_goal=False,  # Don't automatically stop this robot when within goal region
        dt=DT,  # Timestep value
        body_color=(255, 0, 0),  # Set the body color to red
        body_filled=True  # Color in the body,
    )

    levy_robot = LevyAgentConfig(
        config=goal_seeking_robot,  # Copy most of the config from the robot above
        levy_constant=0.6,
        forward_rate=b2p(MAX_FORWARD_SPEED),
        turning_rate=np.radians(5),
        body_color=(255, 255, 0),  # Set the body color to yellow
        body_filled=True,
        stop_at_goal=False,  # Don't stop when the agent is in the goal region...
        stop_on_goal_detect=True,  # ...stop when the agent DETECTS the goal
        curve_based=True  # Indicate that agents should turn while moving forward, rather than just turn in-place
    )

    # Create a Heterogeneous Swarm and add both agent types to it. Ratio of the subpopulations is determined by the value of RATIO_LEVY
    heterogeneous_swarm = HeterogeneousSwarmConfig()
    heterogeneous_swarm.add_sub_populuation(goal_seeking_robot, count=(NUM_AGENTS - int(RATIO_LEVY * NUM_AGENTS)))
    heterogeneous_swarm.add_sub_populuation(levy_robot, count=int(RATIO_LEVY * NUM_AGENTS))

    return heterogeneous_swarm


def establish_metrics():
    metric_0 = PercentageAtGoal(0.01)  # Record the time (timesteps) at which 1% of the agents found the goal
    metric_A = PercentageAtGoal(0.5)  # Record the time (timesteps) at which 50% of the agents found the goal
    metric_B = PercentageAtGoal(0.75)  # Record the time (timesteps) at which 75% of the agents found the goal
    metric_C = PercentageAtGoal(0.90)  # Record the time (timesteps) at which 90% of the agents found the goal
    metric_D = PercentageAtGoal(1.00)  # Record the time (timesteps) at which 100% of the agents found the goal
    metric_E = AgentsAtGoal()  # Record the number of Agents in the Goal Region
    return [metric_0, metric_A, metric_B, metric_C, metric_D, metric_E]

def configure_env(robot_config, size=(500, 500), num_agents=20):
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
        seed=SEED
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
        seed=SEED,
        init_type=starting_region,  # A starting region where agents will spawn at t=0
        goals=[goal_region],  # A list of goals for the robots to find
        collide_walls=True,  # Use No Environment Walls for this problem
        show_walls=False  # Hide Default Walls
    )

    return env


# Get a random controller
def get_random_controller():
    controller = []
    for _ in range(4):
        controller.append(round(random.random(), ndigits=3))
    return controller

# Create a Callback function that will be called at every .step() of the world
# If interfacing is complex enough that is cannot be done in a callback func, use 
def callback(world, screen):
    """
    Read/Write from the world data
    
    Params:
    - world: A World object (see src/novel_swarms/world/) that contains agent information. Can be modified in-place.
    - screen: A pygame screen object that allows for direct read/write of the pixel values in the window
    """

    # Example: READ all agents (x, y, theta) positions.
    # positions = [(agent.x_pos, agent.y_pos, agent.angle) for agent in world.population]

    # Example: READ (Calculate) the number of agents at goal:
    # num_at_goal = sum([int(world.goals[0].agent_achieved_goal(agent)) for agent in world.population])

    # print(positions[0])
    # print(num_at_goal)

    # Example: WRITE random controllers to all agents every frame
    # for agent in world.population:
    #     agent.controller = get_random_controller()

    # Example: WRITE (Change) all agents to be a new shade of red every frame
    # new_color = (int((random.random() * 200) + 55), 0, 0)
    # for agent in world.population:
    #     agent.body_color = new_color


# Main Function
if __name__ == "__main__":
    robot_conf = configure_robots()
    world_conf = configure_env(robot_config=robot_conf, num_agents=NUM_AGENTS, size=(b2p(WORLD_W), b2p(WORLD_H)))
    world_conf.stop_at = 1000
    world_subscriber = WorldSubscriber(func=callback)

    # print(robot_config)

    world_output = simulator(
        world_config=world_conf,
        subscribers=[world_subscriber],
        show_gui=False,
    )
    print(world_output.population[0].x_pos)