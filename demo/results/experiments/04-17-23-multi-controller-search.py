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

def get_world_config(seed, agent, n=30):
    ret = RectangularWorldConfig(
        size=(500, 500),
        n_agents=n,
        seed=seed,
        behavior=[
            AverageSpeedBehavior(),
            AngularMomentumBehavior(),
            RadialVarianceBehavior(),
            ScatterBehavior(),
            GroupRotationBehavior(),
        ],
        agentConfig=agent,
        padding=15,
        stop_at=10000,
        show_walls=True,
        collide_walls=True,
    )
    return ret

def get_data(worlds):
    ret = []
    for world in worlds:
        controller = world.config.agentConfig.controller
        base = [world.seed, world.total_steps]
        base += controller
        for b in world.behavior:
            base.append(b.out_average()[1])
        ret.append(base)
    return ret

def get_sim_config(controllers, seeds, n=30):
    N_AGENTS = n
    agent_config = [
        DiffDriveAgentConfig(
            controller=controller,
            sensors=SensorSet([
                BinaryLOSSensor(angle=0),
            ]),
            seed=seed,
            agent_radius=7
        ) for controller, seed in zip(controllers, seeds)
    ]
    sim_config = [
        get_world_config(a_c.seed, a_c, n=N_AGENTS) for a_c in agent_config
    ]
    return sim_config

def stop_detection_method(world):
    EPSILON = 0.05
    if world.total_steps > 100 and world.behavior[3].out_average()[1] < EPSILON:
        return True
    return False

if __name__ == "__main__":
    processor = MultiWorldSimulation(pool_size=12, single_step=False, with_gui=False)
    controllers = [[i / 10, j / 10, 1.0, -1.0] for i in range(-10, 10, 1) for j in range(-10, 10, 1)]
    seeds = [1 for _ in controllers]

    conf = get_sim_config(controllers, seeds, n=12)
    ret = processor.execute(conf, world_stop_condition=stop_detection_method)
    d = get_data(ret)

    df = DataFrame(d)
    df.columns = ["SEED", "TOTAL_STEPS", "CL0", "CR0", "CL1", "CR1", "AVG_SPEED", "ANG_MOMENTUM", "RADIAL_VARIANCE", "SCATTER", "GROUP_ROTATION"]
    df.to_csv("out/swarm-exploration.csv")



