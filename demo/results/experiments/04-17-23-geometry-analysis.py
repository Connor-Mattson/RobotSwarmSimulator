import numpy as np

from novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal, PercentageAtGoal
from novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
from novel_swarms.world.goals.Goal import AreaGoal
from novel_swarms.world.obstacles.Wall import Wall
from novel_swarms.world.simulate import main as sim
from novel_swarms.behavior.PersistentHomology import PersistentHomology
from novel_swarms.behavior.ConvexHull import ConvexHull, InverseConvexHull
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig, UnicycleAgentConfig, LevyAgentConfig, MazeAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.util.timer import Timer
import matplotlib.pyplot as plt
from pandas import DataFrame

def get_world_config(seed, agent, rm_agent = False, n=30):
    ret = RectangularWorldConfig(
        size=(500, 500),
        n_agents=n,
        seed=seed,
        behavior=[
            ConvexHull(),
            InverseConvexHull(),
            PersistentHomology(dims=0, history_size=10),
            PersistentHomology(dims=1, history_size=10),
            PersistentHomology(dims=0, history_size=10, max_death=True),
            PersistentHomology(dims=1, history_size=10, max_death=True),
        ],
        agentConfig=agent,
        padding=15,
        stop_at=2500,
        show_walls=True,
        collide_walls=True,
    )
    return ret

def get_geometry_data(worlds):
    ret = []
    for world in worlds:
        base = [world.population_size, world.seed, world.total_steps]
        for b in world.behavior:
            base.append(b.out_average()[1])
        ret.append(base)
    return ret

def get_geometry_config(controllers, seeds, n=30):
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
        get_world_config(a_c.seed, a_c, n=N_AGENTS, rm_agent=True) for a_c in agent_config
    ]
    return sim_config


if __name__ == "__main__":
    files = [
        # "../../../data/diffdrivegenomes/aggregation.csv",
        # "../../../data/diffdrivegenomes/cyclic.csv",
        # "../../../data/diffdrivegenomes/dispersal.csv",
        "../../../data/diffdrivegenomes/milling.csv",
        # "../../../data/diffdrivegenomes/wall-following.csv",
    ]
    controller_sets = [
        np.loadtxt(name, delimiter=",", dtype=float) for name in files
    ]
    processor = MultiWorldSimulation(pool_size=12, single_step=False, with_gui=False)

    for name, b_set in zip(files, controller_sets):
        print(f"RUN! {name}")
        seeds = [1 for _ in range(len(b_set))]
        geo_conf = get_geometry_config(b_set, seeds, n=12)
        ret = processor.execute(geo_conf)
        geo_data = get_geometry_data(ret)
        df = DataFrame(geo_data)
        df.to_csv(f"out/geometry-{name[31:]}")



