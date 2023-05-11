from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal, PercentageAtGoal
from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
from src.novel_swarms.world.goals.Goal import CylinderGoal
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig, StaticAgentConfig, UnicycleAgentConfig, LevyAgentConfig, MazeAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
import numpy as np


if __name__ == "__main__":

    AGGREGATION_CONTROLLER = [ 4.3155251,  -0.71469968, -0.43351827,  1.87505216,  2.37840557,  0.41038622]
    SEED = None
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = 10
    # WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)
    WIDTH, HEIGHT = 1000, 1000

    def controller(sensor_states):
        if sensor_states[0] == 0:
            return 0
        if sensor_states[0] == 1:
            return 1
        if sensor_states[0] == 2:
            return 2

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 13.5),
            bias=-4,
            degrees=True,
            false_positive=0.0,
            false_negative=0.0,
            # Rectangle Representing Environment Boundaries
            walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
            wall_sensing_range=(BL * 4),
            time_step_between_sensing=2,
            goal_sensing_range=(BL * 29.13),
            detect_goal_with_added_state=True,
        )
    ],
    custom_state_decision=controller)

    base_config = UnicycleAgentConfig(
        controller=AGGREGATION_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True,
        body_filled=True,
        body_color=(255, 0, 0),
        trace_length=500,
        trace_color=(255, 255, 255)
    )

    agent_levy = LevyAgentConfig(
        base_config,
        levy_constant="Random",
        turning_rate=2.0,
        forward_rate=12.5,
        step_scale=30.0,
        seed=None,
    )

    agent_maze = MazeAgentConfig(
        controller=AGGREGATION_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=True,
        body_filled=True,
        body_color=(255, 0, 0),
        stop_at_goal=False,
    )

    agent_config_b = UnicycleAgentConfig(
        controller=AGGREGATION_CONTROLLER,
        agent_radius=BL / 2,
        dt=0.13,  # 130ms sampling period
        sensors=sensors,
        seed=None,
        idiosyncrasies=False,
        body_filled=True,
        body_color=(255, 0, 0)
    )

    heterogeneous_swarm_config = HeterogeneousSwarmConfig()
    heterogeneous_swarm_config.add_sub_populuation(agent_levy, 0)
    heterogeneous_swarm_config.add_sub_populuation(agent_maze, 10)

    behavior = [
        TotalCollisionsBehavior(),
        DistanceToGoal(),
        AgentsAtGoal(history=1),
        PercentageAtGoal(0.01, history=1),
        PercentageAtGoal(0.80, history=1),
        PercentageAtGoal(1.0, history=1),
    ]

    goals = [CylinderGoal(250, 200, 20, remove_agents_at_goal=True, range=100)]
    objects = []

    initial_conditions = [(500, 900, np.random.random() * 2 * np.pi) for i in range(N_AGENTS)]

    world_config = RectangularWorldConfig(
        size=(WIDTH, HEIGHT),
        n_agents=10,
        seed=SEED,
        behavior=behavior,
        show_walls=True,
        collide_walls=True,
        agent_initialization=initial_conditions,
        agentConfig=heterogeneous_swarm_config,
        padding=15,
        objects=objects,
        goals=goals,
    )

    # def stop_when(world):
    #     if world.total_steps > 100 and world.behavior[0].out_average()[1] == 0:
    #         return True
    #     return False
    #
    # time_to_goal = []
    # for i in range(100):
    #     world = simulate(world_config=world_config, stop_detection=stop_when, step_size=10)
    #     time_to_goal.append(world.total_steps)
    #     print(time_to_goal)

    world = simulate(world_config=world_config, step_size=2)