from typing import Tuple

from src.novel_swarms.novelty.GeneRule import GeneRuleContinuous
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
import time
import numpy as np
import pandas as pd

def get_rand(mag):
    return ((np.random.random() * 2) - 1) * mag

if __name__ == "__main__":
    controllers = []
    behaviors = []
    class_labels = []

    try:
        for i in range(400):
            genotype = [
                GeneRuleContinuous(_max=27.0, _min=-27.0, mutation_step=3, round_digits=3, exclude=[[-15, 15]]),
                GeneRuleContinuous(_max=1.6, _min=-1.6, mutation_step=0.6, round_digits=3, exclude=[[-0.4, 0.4]]),
                GeneRuleContinuous(_max=27.0, _min=-27.0, mutation_step=3, round_digits=3, exclude=[[-15, 15]]),
                GeneRuleContinuous(_max=1.6, _min=-1.6, mutation_step=0.6, round_digits=3, exclude=[[-0.4, 0.4]]),
            ]
            CONTROLLER = [g.fetch() for g in genotype]

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
                dt=0.1,
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

            ret = None
            while sim.world.total_steps < 605 and ret is None:
                ret = sim.step(per_step_draw=True)

            if ret is None:
                while ret is None:
                    ret = sim.step(per_step_draw=True, stall=True)

            if isinstance(ret, Tuple):
                print(ret)
                label, steps = ret
                controllers.append(CONTROLLER)
                b = sim.world.getBehaviorVector()
                behaviors.append(b)
                class_labels.append(label)
            else:
                print("Did not save the data to the file, bad output!")

    except KeyboardInterrupt:
        print("Keyboard Interrupt thrown! Saving data before termination...")

    COLUMNS = ["class"] + [f"controller_{i}" for i in range(len(controllers[0]))] + [f"behavior_{i}" for i in range(len(behaviors[0]))]

    controller_df = pd.DataFrame(controllers)
    behavior_df = pd.DataFrame(behaviors)
    class_labels_df = pd.DataFrame(class_labels)
    df = pd.concat([class_labels_df, controller_df, behavior_df], axis=1)
    df.columns = COLUMNS
    df.to_csv(f"labeled_classes_{int(time.time())}.csv", index=True)
