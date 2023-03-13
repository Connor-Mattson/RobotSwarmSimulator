from graphing_results import METRIC_LIST, convert_data_to_weighted_average

from novel_swarms.world.WorldFactory import WorldFactory
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig

import os
import shutil
import csv
from statistics import mean
from functools import reduce
from random import randint
import matplotlib.pyplot as plt

# Paths to access files
ROOT_PATH = os.path.abspath("../..")
DATA_PATH = os.path.join(ROOT_PATH, "data/entropic_data/")
# Varied light colors for random samples
SAMPLE_COLORS = ["#FBC9BE", "#FDEAB8", "#D2FDB5", "#B5FDF8", "#C8B5FD"]

# Scale the controller linearly such that the largest element in the controller is 1 or -1
def normalize_controller(c):
    absolute_controller = [abs(x) for x in c]
    scaling_factor = 1 / max(absolute_controller)
    return [x * scaling_factor for x in c]

# List of entropic controllers
entropic_controller_list = list()

# Populate entropic_controller_list with only the random controllers
# Thanos-snap 3/4 of them out of existence because it's overpopulated and redundant
with open(os.path.join(ROOT_PATH, "data/testing_labels.csv"), "r") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        numerical_row = [float(x) for x in row]
        is_random = numerical_row[0] == 0
        if is_random and i % 4 == 0:
            entropic_controller_list.append(numerical_row[1:])

if __name__ == '__main__':
    print(entropic_controller_list[0])
    print("(O/N): Do you want to use pre-existing old data (O) or collect new data (N)?")
    user_answer = input()

    if user_answer == 'N':

        # Purge and replace data directory since we are collecting new data
        if os.path.exists(DATA_PATH):
            shutil.rmtree(DATA_PATH)
        os.mkdir(DATA_PATH)

        # For every controller in the list of entropic controllers, collect behavior data for all metrics
        print("Starting data collection.")
        for i, controller in enumerate(entropic_controller_list):
            # Create a world with the controller
            sensors = SensorSet([BinaryLOSSensor(angle=0)])
            agent_config = DiffDriveAgentConfig(
                controller=controller,
                sensors=sensors,
                seed=None
            )

            behavior = None

            world_config = RectangularWorldConfig(
                size=(500, 500),
                n_agents=30,
                seed=None,
                behavior=behavior,
                agentConfig=agent_config,
                padding=15
            )

            # Simulate the world with the genome
            # All metrics are tracked until the world is exited
            world = WorldFactory.create(world_config)
            positions_list = list()
            velocities_list = list()
            counter = 0
            for j in range(1200):
                world.step()
            for j in range(1200, 3000):
                world.step()
                # Only record data every five frames to save time
                if j % 5 == 0:
                    counter += 1
                    # Get positions and velocities of all agents at the frame
                    current_positions = world.get_all_positions()
                    positions_list.append(current_positions)
                    current_velocities = world.get_all_velocities()
                    velocities_list.append(current_velocities)

            progress = (i + 1) / len(entropic_controller_list) * 100
            print(f"Progress: {str(progress)[:5]}%")

            def write_to_file(path, arr):
                with open(path, "a") as f:
                    writer = csv.writer(f, delimiter=',')
                    for experiment in arr:
                        for frame in experiment:
                            writer.writerow(frame)
                        writer.writerow(["New"])

            velocities_file_path = os.path.join(DATA_PATH, "velocities.csv")
            positions_file_path = os.path.join(DATA_PATH, "positions.csv")
            write_to_file(velocities_file_path, velocities_list)
            write_to_file(positions_file_path, positions_list)
        print("Data collection has ended.")
    
    # Data collection has ended.

    # Data processing begins.

    for metric in METRIC_LIST:
        file_path = os.path.join(DATA_PATH, metric.name + ".csv")
        data = list()

        # Open the file storing the metric data
        with open(file_path, "r") as file:
            reader = csv.reader(file)

            # For the whole metric data file, add each row of behavior data to the `data` list
            for row in reader:
                numerical_row = [float(x) for x in row]
                dataset = convert_data_to_weighted_average(numerical_row, 5)
                data.append(list(dataset))

        # Get lower and upper bound lines, along with their corresponding controllers
        lower_bound_line = data[0]
        upper_bound_line = data[0]
        lower_bound_controller = None
        upper_bound_controller = None
        for i in range(1, len(data)):
            if mean(data[i]) < mean(lower_bound_line):
                lower_bound_line = data[i]
                lower_bound_controller = entropic_controller_list[i]
            if mean(data[i]) > mean(upper_bound_controller):
                upper_bound_line = data[i]
                upper_bound_controller = entropic_controller_list[i]

        # Get the range of the graph for the purposes of presentation
        largest_y = list(reduce(lambda a, b: a if max(a) > max(b) else b, data))
        smallest_y = list(reduce(lambda a, b: a if min(a) < min(b) else b, data))

        line_samples = list()
        sample_controllers = list()

        for _ in range(5):
            i = randint(0, len(data))
            sample = data[i]
            controller = entropic_controller_list[i]
            if sample not in line_samples and sample != lower_bound_line and sample != upper_bound_line:
                line_samples.append(list(sample))

        fig, ax = plt.subplots()
        ax.set_xlabel("Timesteps")
        ax.set_ylabel(metric.name)
        ax.setTitle(f"{metric.name} data samples for various entropic controllers")
        ax.legend(loc='upper right', bbox_to_anchor=(1.04, 1))
        ax.axis([1200, 1200+len(largest_y), smallest_y, largest_y])
        ax.set_ylim(smallest_y, largest_y)

        ax.plot(
            lower_bound_line,
            label=f"Lower Bound: {lower_bound_controller}",
            color='blue',
            linewidth=2,
            linestyle='',
            marker='o',
            markersize=1
        )
        ax.plot(
            upper_bound_line,
            label=f"Upper Bound: {upper_bound_controller}",
            color='red',
            linewidth=2,
            linestyle='',
            marker='o',
            markersize=1
        )
        for i in range(5):
            ax.plot(
                line_samples[i],
                label=sample_controllers[i],
                color=SAMPLE_COLORS[i],
                linewidth=2,
                linestyle='',
                marker='o',
                markersize=1
            )
        chart_path = os.path.join(DATA_PATH, metric.name)
        fig.tight_layout()
        fig.savefig(chart_path)

"""
After 1200 timesteps...
0: Random
1: Cyclic
2: Milling
3: Aggregation
4: Dispersal
5: Wall following
"""