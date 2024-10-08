from src.novel_swarms.world.initialization.GridInit import GridInitialization
from src.novel_swarms.world.simulate import Simulation
from src.novel_swarms.behavior import *
from src.novel_swarms.behavior.ConvexHull import ConvexHull
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig, HeroRobotConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.gui.abstractGUI import AbstractGUI
import random
import numpy as np
import pandas as pd

def get_rand(mag):
    return ((np.random.random() * 2) - 1) * mag

if __name__ == "__main__":
    controllers = []
    behaviors = []

    for i in range(1000):
        CONTROLLER = [get_rand(5), get_rand(1), get_rand(5), get_rand(1)]
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
            dt=0.5,
        )

        behavior = [
            AverageSpeedBehavior(),
            AngularMomentumBehavior(),
            RadialVarianceBehavior(),
            ScatterBehavior(),
            GroupRotationBehavior(),
            TotalCollisionsBehavior(),
            ConvexHull(),
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
            stop_at=None,
        )

        sim = Simulation(world_config=world_config, save_duration=500, save_every_ith_frame=5, gui=AbstractGUI(), show_gui=True)

        for s in range(1510):
            ret = sim.step(per_step_draw=True)
            if ret is not None:
                break
            if s == 1000:
                b = sim.world.getBehaviorVector()
                print("Behavior Vector:", b)
                if b[0] < 0.05:
                    print("This is WAY too slow!")
                sim.record_gif()
        controllers.append(CONTROLLER)
        b = sim.world.getBehaviorVector()
        behaviors.append(b)
    COLUMNS = [f"controller_{i}" for i in range(len(controllers[0]))] + [f"behavior_{i}" for i in range(len(behaviors[0]))]

    # controller_df = pd.DataFrame(controllers)
    # behavior_df = pd.DataFrame(behaviors)
    # df = pd.concat([controller_df, behavior_df], axis=1)
    # df.columns = COLUMNS
    # df.to_csv("metadata.csv", index=True)
