import os
from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.agent.MazeAgent import MazeAgent
from src.novel_swarms.agent.control.Controller import Controller
import numpy as np

ZOOM = 10

def milling_controller(agent: MazeAgent):
    """
    An example of a "from scratch" controller that you can code with any information contained within the agent class
    """
    sigma = agent.goal_seen  # Whether the goal has been detected previously by this agent
    gamma = agent.agent_in_sight is not None  # Whether the agent detects another agent

    u_1, u_2 = 0.0, 0.0  # Set these by default
    if not sigma:
        if not gamma:
            u_1, u_2 = 10, np.radians(15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
        else:
            u_1, u_2 = 10, np.radians(-15)  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    else:
        u_1, u_2 = 0.0, 0.0  # u_1 in pixels/second (see b2p func), u_2 in rad/s
    return u_1, u_2

def robot_setup():
    goal_agent = AgentYAMLFactory.from_yaml("../../../demo/configs/flockbots-icra/goalbot.yaml")
    levy_agent = AgentYAMLFactory.from_yaml("../../../demo/configs/flockbots-icra/levy.yaml")

    goal_agent.controller = Controller(milling_controller)

    heterogeneous_swarm = HeterogeneousSwarmConfig()
    heterogeneous_swarm.add_sub_populuation(goal_agent, count=5)
    heterogeneous_swarm.add_sub_populuation(levy_agent, count=5)
    heterogeneous_swarm.factor_zoom(zoom=ZOOM)
    return goal_agent

def world_setup():
    world = WorldYAMLFactory.from_yaml("../../../demo/configs/flockbots-icra/world.yaml")

    init = FixedInitialization("../../../demo/configs/flockbots-icra/init_translated.csv")
    world.init_type = init
    world.population_size = 30

    world.factor_zoom(zoom=ZOOM)
    world.addAgentConfig(robot_setup())
    return world

if __name__ == "__main__":
    w = world_setup()
    sim(w, start_paused=True)
