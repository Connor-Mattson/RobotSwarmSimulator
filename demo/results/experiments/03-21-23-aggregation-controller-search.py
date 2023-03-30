import numpy as np

from novel_swarms.world.simulate import main as simulate
from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
import matplotlib.pyplot as plt
import seaborn as sns
import random
from pandas import DataFrame

def simulate_and_ret(controller, stop_detection, max_steps=3000, seed=1):
    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=controller,
        sensors=sensors,
        seed=seed,
    )

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=14,
        seed=seed,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        stop_at=max_steps
    )

    world = simulate(world_config=world_config, stop_detection=stop_detection, step_size=16)
    if world.total_steps >= max_steps:
        return False, world
    return True, world


def stop_detection_method(world):
    EPSILON = 0.05
    if world.total_steps > 100 and world.behavior[3].out_average()[1] < EPSILON:
        return True
    return False


if __name__ == "__main__":
    for seed in range(2, 10, 1):
        v_l_1, v_r_1 = 1.0, -1.0
        output_A = np.zeros((21, 21))
        output_B = np.zeros((21, 21))

        x_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 1)]
        y_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 1)]

        for i in range(0, 21, 1):
            v_l_0 = round((i - 10) * 0.1, 1)
            for j in range(0, 21, 1):
                v_r_0 = round((j - 10) * 0.1, 1)
                controller = [v_l_0, v_r_0, v_l_1, v_r_1]
                cyclic, w = simulate_and_ret(controller, stop_detection_method, max_steps=2500, seed=seed)
                print(f"Detection? - {cyclic}")
                output_A[i][j] = w.total_steps
                output_B[i][j] = -w.behavior[3].out_average()[1]

        df = DataFrame(output_A)
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(df, annot=False, ax=ax, square=True)
        ax.set_xticklabels(x_tick_labels)
        ax.set_yticklabels(y_tick_labels)
        ax.set_xlabel("$V_{r0}$")
        ax.set_ylabel("$V_{l0}$")
        plt.title("Simulation Time (Max: 2500)")
        plt.tight_layout()
        df.to_csv(f"out/sim-time-aggregation-s{seed}.csv")
        plt.show()