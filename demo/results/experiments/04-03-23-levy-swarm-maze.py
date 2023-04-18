from novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal, PercentageAtGoal
from novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from novel_swarms.world.goals.Goal import AreaGoal
from novel_swarms.world.obstacles.Wall import Wall
from novel_swarms.world.simulate import main as sim
from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig, UnicycleAgentConfig, LevyAgentConfig, MazeAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.util.timer import Timer
import matplotlib.pyplot as plt
from pandas import DataFrame

def get_world_config(seed, agent, rm_agent = False, n=30):
    goals = [AreaGoal(200, 200, 75, 20, remove_agents_at_goal=rm_agent)]
    objects = [
        Wall(None, 180, 193, 120, 2),
        Wall(None, 180, 193, 2, 91),
        Wall(None, 300, 193, 2, 91),
        Wall(None, 240, 350, 2, 135),
    ]
    ret = RectangularWorldConfig(
        size=(500, 500),
        n_agents=n,
        seed=seed,
        behavior=[
            DistanceToGoal(),
            AgentsAtGoal(history=1),
            PercentageAtGoal(0.01, history=1),
            PercentageAtGoal(0.10, history=1),
            PercentageAtGoal(0.25, history=1),
            PercentageAtGoal(0.50, history=1),
            PercentageAtGoal(0.80, history=1),
            PercentageAtGoal(0.90, history=1),
            PercentageAtGoal(0.95, history=1),
            PercentageAtGoal(1.0, history=1),
        ],
        agentConfig=agent,
        padding=15,
        stop_at=10000,
        objects=objects,
        goals=goals,
        show_walls=True,
        collide_walls=True,
    )
    return ret

def get_levy_data(worlds):
    ret = []
    for world in worlds:
        base = [world.population_size, world.seed, world.meta["levy_value"], world.total_steps]
        for b in world.behavior:
            base.append(b.out_average()[1])
        ret.append(base)
    return ret

def get_milling_data(worlds):
    ret = []
    for world in worlds:
        base = [world.population_size, world.seed, world.total_steps]
        for b in world.behavior:
            base.append(b.out_average()[1])
        ret.append(base)
    return ret

def get_levy_config(seeds, n=30):
    AGGREGATION_CONTROLLER = [12.5, 0.5, 12.5, -0.5]
    BL = 14
    N_AGENTS = n
    agent_config = [
        LevyAgentConfig(
            UnicycleAgentConfig(
                controller=AGGREGATION_CONTROLLER,
                agent_radius=BL / 3,
                dt=0.13,  # 130ms sampling period
                sensors=SensorSet([
                    BinaryFOVSensor(
                        theta=14 / 2,
                        bias=-4,
                        degrees=True,
                        false_positive=0.0,
                        false_negative=0.0,
                        time_step_between_sensing=2,
                    )
                ]),
                seed=seed,
                idiosyncrasies=True,
            ),
            levy_constant="Random",
            turning_rate=2.0,
            forward_rate=12.5,
            step_scale=30.0,
            seed=seed,
        ) for seed in seeds
    ]
    sim_config = [
        get_world_config(a_c.seed, a_c, n=N_AGENTS, rm_agent=True) for a_c in agent_config
    ]
    return sim_config

def get_milling_config(seeds, n=30):
    AGGREGATION_CONTROLLER = [12.5, 0.5, 12.5, -0.5]
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = n
    WIDTH, HEIGHT = int(BL * 29.8), int(BL * 29.8)
    agent_config = [
        MazeAgentConfig(
            controller=AGGREGATION_CONTROLLER,
            agent_radius=BL / 3,
            dt=0.13,  # 130ms sampling period
            sensors=SensorSet([
                BinaryFOVSensor(
                    theta=14,
                    distance=(BL * 8),
                    bias=-4,
                    degrees=True,
                    false_positive=0.10,
                    false_negative=0.05,
                    # Rectangle Representing Environment Boundaries
                    walls=[[GUI_PADDING, GUI_PADDING], [GUI_PADDING + WIDTH, GUI_PADDING + HEIGHT]],
                    wall_sensing_range=(BL * 4),
                    time_step_between_sensing=2,
                )
            ]),
            seed=seed,
            idiosyncrasies=True,
        ) for seed in seeds
    ]
    sim_config = [
         get_world_config(a_c.seed, a_c, n=N_AGENTS) for a_c in agent_config
    ]
    return sim_config

def stop_early(world):
    if len(world.population) == 0:
        return True
    if world.total_steps > 0:
        if world.behavior[-1].out_average()[1] >= 0:
            return True
        if world.behavior[1].out_current()[1] == len(world.population):
            return True
    return False

if __name__ == "__main__":
    seeds = range(0, 50, 1)
    n_agents = range(1, 31, 1)
    processor = MultiWorldSimulation(pool_size=12, single_step=False, with_gui=False)

    milling_data = []
    levy_data = []
    for n in n_agents:
        # Milling Agents
        mil_conf = get_milling_config(seeds, n=n)
        ret = processor.execute(mil_conf, world_stop_condition=stop_early)
        d = get_milling_data(ret)
        print(d)
        milling_data += d

        # Levy Agents
        levy_conf = get_levy_config(seeds, n=n)
        ret = processor.execute(levy_conf, world_stop_condition=stop_early)
        d = get_levy_data(ret)
        print(d)
        levy_data += d

    df = DataFrame(milling_data)
    df.to_csv("out/swarm-solvers.csv")

    df = DataFrame(levy_data)
    df.to_csv("out/levy-solvers.csv")



