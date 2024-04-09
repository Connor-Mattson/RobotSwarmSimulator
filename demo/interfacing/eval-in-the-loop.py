"""
Example Script
The SwarmSimulator allows control of the world and agents at every step within the main loop
"""
import math
import random
import numpy as np
import random

# Import Agent embodiments
from src.novel_swarms.config.AgentConfig import *
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.agent.MazeAgent import MazeAgent

# Import FOV binary sensor
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor

# Import Rectangular World Data, Starting Region, and Goal Region
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig, WorldYAMLFactory
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

# import numpy as np
SEED = 20
# np.random.seed(SEED)
# random.seed(SEED)


# Seeding for initial Starting positions, FP/FN Readings.
SCALE = 10  # Set the conversion factor for Body Lengths to pixels (all metrics will be scaled appropriately by this value)
N, T = 10, 1000  # Number of agents, N, and timestep limit, T.


def custom_controller(agent: MazeAgent):
    """
    An example of a "from scratch" controller that you can code with any information contained within the agent class
    """
    sigma = agent.goal_seen  # Whether the goal has been detected previously by this agent
    gamma = agent.agent_in_sight is not None  # Whether the agent detects another agent

    u_1, u_2 = 0.0, 0.0  # Set these by default
    if not sigma:
        if not gamma:
            u_1, u_2 = 1.0 * SCALE, 1.0  # u_1 in pixels/second (BL/sec * SCALE), u_2 in rad/s
        else:
            u_1, u_2 = 1.0 * SCALE, -1.0  # u_1 in pixels/second (BL/sec * SCALE), u_2 in rad/s
    else:
        u_1, u_2 = 0.0, 0.0  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    return u_1, u_2

def configure_robots():
    """
    Select the Robot's Sensors and Embodiment, return the robot configuration
    """
    # Import the Goal Agent data from YAML
    goal_seeking_robot = AgentYAMLFactory.from_yaml("../../demo/configs/flockbots-icra/goalbot.yaml")
    goal_seeking_robot.rescale(SCALE)

    # Import the flockbot data from YAML
    normal_flockbot = AgentYAMLFactory.from_yaml("../../demo/configs/flockbots-icra-milling/flockbot.yaml")
    # normal_flockbot.controller = Controller(custom_controller)
    normal_flockbot.controller = Controller([10.21016141691062,0.34394605572151926,9.90100680343106,0.10310121227494662])
    normal_flockbot.seed = SEED

    # Uncomment to remove FN/FP from agents (Testing)
    # normal_flockbot.sensors.sensors[0].fn = 0.0
    # normal_flockbot.sensors.sensors[0].fp = 0.0

    normal_flockbot.rescale(SCALE)  # Convert all the BodyLength measurements to pixels in config
    return normal_flockbot


def establish_goal_metrics():
    metric_0 = PercentageAtGoal(0.01)  # Record the time (timesteps) at which 1% of the agents found the goal
    metric_A = PercentageAtGoal(0.5)  # Record the time (timesteps) at which 50% of the agents found the goal
    metric_B = PercentageAtGoal(0.75)  # Record the time (timesteps) at which 75% of the agents found the goal
    metric_C = PercentageAtGoal(0.90)  # Record the time (timesteps) at which 90% of the agents found the goal
    metric_D = PercentageAtGoal(1.00)  # Record the time (timesteps) at which 100% of the agents found the goal
    metric_E = AgentsAtGoal()  # Record the number of Agents in the Goal Region
    return [metric_0, metric_A, metric_B, metric_C, metric_D, metric_E]

def establish_milling_metrics():
    # TODO: Update this value with Kevin's Formulation
    # circliness = RadialVarianceBehavior()
    # circliness = Circliness(history=450)
    circliness = Circliness(avg_history_max=450)
    return [circliness, TotalCollisionsBehavior()]

def configure_env(robot_config, num_agents=20, seed=None):
    # search_and_rendezvous_world = WorldYAMLFactory.from_yaml("demo/configs/flockbots-icra/world.yaml")

    # Import the world data from YAML
    world = WorldYAMLFactory.from_yaml("../../demo/configs/flockbots-icra-milling/world.yaml")
    # world.seed = seed
    world.addAgentConfig(robot_config)
    world.population_size = num_agents
    world.factor_zoom(SCALE)
    world.behavior = establish_milling_metrics()
    return world

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


def stop_on_collision(world):
    if world.behavior[1].out_average()[1] > 20:
        return True
    return False

# Main Function
if __name__ == "__main__":
    robot_conf = configure_robots()
    world_conf = configure_env(robot_config=robot_conf, num_agents=N, seed=SEED)
    world_conf.stop_at = 1000
    # world_subscriber = WorldSubscriber(func=callback)

    # print(robot_config)

    world_output = simulator(
        world_config=world_conf,
        # subscribers=[world_subscriber],
        show_gui=True,
        save_every_ith_frame=2,
        save_duration=1000,
        # stop_detection=stop_on_collision
    )
