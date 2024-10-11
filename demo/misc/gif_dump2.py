import os

from src.novel_swarms.world.initialization.GridInit import GridInitialization
from src.novel_swarms.world.simulate import Simulation
from src.novel_swarms.world.RectangularWorld import RectangularWorld
from src.novel_swarms.behavior import *
from src.novel_swarms.behavior.ConvexHull import ConvexHull
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig, HeroRobotConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.gui.abstractGUI import AbstractGUI
from src.novel_swarms.util.processing.multicoreprocessing import MultiWorldSimulation
import random
import numpy as np

from src.novel_swarms.world.subscribers.World2Gif import World2Gif
import pandas as pd

def stop(w: RectangularWorld):
    if w.total_steps > 100 and (w.getBehaviorVector()[-1] > 0.6 or w.getBehaviorVector()[0] < 0.4):
        print("Found dud, popping!")
        return True
    return False

def get_rand(mag):
    return ((np.random.random() * 2) - 1) * mag

if __name__ == "__main__":
    controllers = []
    behaviors = []
    world_configs = []

    for i in range(2200):
        CONTROLLER = [get_rand(10), get_rand(1), get_rand(10), get_rand(1)]
        print("*" * 40)
        print("Iter", i)
        print("*" * 40)
        print(CONTROLLER)

        sensors = SensorSet([
            BinaryFOVSensor(theta=0.12, distance=100 * 3, show=False),
        ])

        agent_config = HeroRobotConfig(
            controller=CONTROLLER,
            sensors=sensors,
            trace_length=0,
            body_filled=True,
            dt=0.25,
        )

        behavior = [
            AverageSpeedBehavior(),
            AngularMomentumBehavior(),
            RadialVarianceBehavior(),
            ScatterBehavior(),
            GroupRotationBehavior(),
            TotalCollisionsBehavior(),
            ConvexHull(show=False),
        ]

        num_agents = 8
        world_config = RectangularWorldConfig(
            size=(171 * 3, 142 * 3),
            n_agents=num_agents,
            seed=0,
            behavior=behavior,
            agentConfig=agent_config,
            padding=15,
            init_type=GridInitialization(
                num_agents=num_agents,
                grid_size=(4, 3),
                bb=((25 * 3, 30 * 3), (146 * 3, 111 * 3))
            ),
            stop_at=605,
            metadata={
                "id": i
            }
        )

        world_configs.append(world_config)


    ret = MultiWorldSimulation(pool_size=12).execute(world_configs, world_stop_condition=stop, batched=False)
    print(len(ret))

    ret = list(filter(lambda x: os.path.exists(f"{x.meta['id']}.gif"), ret))
    print(len(ret))
    behaviors = [w.getBehaviorVector() for w in ret]
    controllers = [w.population[0].controller for w in ret]

    COLUMNS = ["identifier"] + [f"controller_{i}" for i in range(len(controllers[0]))] + [f"behavior_{i}" for i in range(len(behaviors[0]))]

    ids_df = pd.DataFrame([w.meta["id"] for w in ret])
    controller_df = pd.DataFrame(controllers)
    behavior_df = pd.DataFrame(behaviors)
    df = pd.concat([ids_df, controller_df, behavior_df], axis=1)
    df.columns = COLUMNS
    df.to_csv("metadata.csv", index=True)

    # Rename the gifs in this folder to be sequential [1, n], make sure they map to the correct index in the df
    id_df = df["identifier"].to_numpy()
    for i in range(len(id_df)):
        try:
            os.rename(f"{id_df[i]}.gif", f"{i}.gif")
        except Exception as e:
            print("Error in rename", e)
