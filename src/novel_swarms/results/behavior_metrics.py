import numpy as np
from matplotlib import pyplot, colors
import os
from ..world.RectangularWorld import RectangularWorld


def categorized_box_plot():
    print(os.getcwd())

    from src.novel_swarms.util import DiffDriveDataset

    SAMPLE_SIZE = 20
    TIMESTEPS = 3000
    POPULATION = 30

    # SAMPLE_SIZE = 20
    # TIMESTEPS = 10
    # POPULATION = 30

    METRICS = ["Average Speed", "Angular Momentum", "Radial Variance", "Scatter", "Group Rotation"]
    DATA_LABELS = ["Aggregation", "Cylic Pursuit", "Milling", "Dispersal", "Wall Following", "Random"]

    datasets = [
        DiffDriveDataset.AGGREGATION,
        DiffDriveDataset.CYCLIC_PURSUIT,
        DiffDriveDataset.MILLING,
        DiffDriveDataset.DISPERSAL,
        DiffDriveDataset.WALL_FOLLOWING,
        DiffDriveDataset.RANDOM
    ]

    collected = {}

    for dataset in datasets:
        behavior_vectors = []
        print(f"Simulating environments for {dataset.name}")

        sample_indices = np.random.choice([i for i in range(len(dataset.data))], size=SAMPLE_SIZE)
        samples = []
        for index in sample_indices:
            samples.append(dataset.data[index])

        for i, sample in enumerate(samples):
            print(f"Trial {i}")
            world = RectangularWorld(
                w=500, h=500,
                pop_size=POPULATION,
            )
            world.setup(controller=sample)
            for step in range(TIMESTEPS):
                world.step()

            behavior_vectors.append(world.getBehaviorVector())

        behavior_vectors = np.array(behavior_vectors)
        # behavior_vectors = np.transpose(behavior_vectors)
        collected[dataset.name] = behavior_vectors

    print("Simulation Complete")

    for i, behavior_metric in enumerate(METRICS):
        metrics = []
        for behavior_pattern in collected:
            # metrics.append(collected[behavior_pattern][:, i])
            metrics.append(np.absolute(collected[behavior_pattern][:, i]))

        pyplot.title(f"{behavior_metric} Categorized by Emergent Behavior")
        pyplot.xlabel(behavior_metric)
        pyplot.ylabel("Emergent Behavior")

        pyplot.boxplot(
            metrics,
            vert=False,
            labels=DATA_LABELS
        )
        pyplot.yticks([1,2,3,4,5,6], DATA_LABELS, rotation=20)
        pyplot.tight_layout()
        pyplot.show()


def categorized_line_plot():
    from src.novel_swarms.util import DiffDriveDataset

    SAMPLE_SIZE = 20
    TIMESTEPS = 4000
    POPULATION = 30

    METRICS = ["Average Speed", "Angular Momentum", "Radial Variance", "Scatter", "Group Rotation"]
    DATA_LABELS = ["Aggregation", "Cylic Pursuit", "Milling", "Dispersal", "Wall Following", "Random"]

    datasets = [
        DiffDriveDataset.AGGREGATION,
        DiffDriveDataset.CYCLIC_PURSUIT,
        DiffDriveDataset.MILLING,
        DiffDriveDataset.DISPERSAL,
        DiffDriveDataset.WALL_FOLLOWING,
        DiffDriveDataset.RANDOM
    ]

    collected = {}

    for dataset in datasets:

        print(f"Simulating environments for {dataset.name}")

        sample_indices = np.random.choice([i for i in range(len(dataset.data))], size=SAMPLE_SIZE)
        samples = []
        for index in sample_indices:
            samples.append(dataset.data[index])

        behavior_at_t_sum = np.array([[0.0 for j in range(5)] for _ in range(TIMESTEPS)])
        for i, sample in enumerate(samples):
            print(f"Trial {i}")
            world = RectangularWorld(
                w=500, h=500,
                pop_size=POPULATION,
            )
            world.setup(controller=sample, seed=i, behavior_history_size=100)
            for step in range(TIMESTEPS):
                world.step()
                behavior_at_t_sum[step] += world.getBehaviorVector()

        behavior_at_t_average = behavior_at_t_sum / len(samples)
        collected[dataset.name] = behavior_at_t_average

    print("Simulation Complete")

    for i, behavior_metric in enumerate(METRICS):
        metrics = []
        for behavior_pattern in collected:
            # metrics.append(collected[behavior_pattern][:, i])
            metrics.append(np.absolute(collected[behavior_pattern][:, i]))

        pyplot.title(f"{behavior_metric} Categorized by Emergent Behavior")
        pyplot.ylabel(behavior_metric)
        pyplot.xlabel("Timesteps")

        for j, pattern in enumerate(DATA_LABELS):
            pyplot.plot(metrics[j], label=pattern)

        pyplot.tight_layout()
        pyplot.legend()
        pyplot.show()


if __name__ == "__main__":
    categorized_line_plot()
