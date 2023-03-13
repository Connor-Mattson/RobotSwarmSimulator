# READ BEFORE RUNNING
# This file must be run from the top level of the project
# The `total_allowed_steps` variable in simulate.py must not be `None`
# Change `total_allowed_steps` back to `None` after running this file
# I know it's hacky, but it works for now

from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.Squareness import SquarenessBehavior
from novel_swarms.behavior.LargestSeparation import LargestSeparationBehavior

from novel_swarms.world.WorldFactory import WorldFactory
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.gui.agentGUI import DifferentialDriveGUI


import os
import shutil
from collections import namedtuple
import csv
import matplotlib.pyplot as plt

Genome = namedtuple("Genome", "name controller")
Metric = namedtuple("Metric", "name content")
ROOT_PATH = os.path.abspath("../..")

GENOME_LIST = [
    Genome('aggregation', [-0.7, -1.0, 1.0, -1.0]),
    Genome('entropic', [-0.83, -0.75, 0.27, -0.57]),
    Genome('wall-following', [1.0, 0.98, 1.0, 1.0]),
    Genome('cyclic-pursuit', [-0.7, 0.3, 1.0, 1.0]),
    Genome('dispersal', [0.2, 0.7, -0.5, -0.1]),
    Genome('milling', [-0.942, -0.592, -1.0, -0.132])
    ]

METRIC_LIST = [
    Metric('angular-momentum', AngularMomentumBehavior),
    Metric('average-speed', AverageSpeedBehavior),
    Metric('group-rotation', GroupRotationBehavior),
    Metric('radial-variance', RadialVarianceBehavior),
    Metric('squareness', SquarenessBehavior),
    Metric('largest-separation', LargestSeparationBehavior)
]

convergence_dict = {
    'aggregation': 450,
    'entropic': None,
    'wall-following': 260,
    'cyclic-pursuit': 650,
    'dispersal': 320,
    'milling': None
}

line_color_dict = {
    'angular-momentum': 'red',
    'average-speed': 'blue',
    'group-rotation': 'brown',
    'radial-variance': 'purple',
    'squareness': 'green',
    'largest-separation': 'pink'
}

def get_genome_file_path(genome):
    return os.path.join(ROOT_PATH, "data/behavior_data/" + genome.name + ".csv")

def get_genome_chart_path(genome):
    return os.path.join(ROOT_PATH, "data/behavior_data/" + genome.name)

def convert_data_to_weighted_average(data, window_size):
    new_data = list()
    for i in range(len(data)):
        window = None
        if i < window_size:
            window = data[:i+1]
        else:
            window = data[i-window_size:i+1]
        window_average = sum(window) / len(window)
        new_data.append(window_average)
    return new_data

def purge_data_dir():
    data_path = os.path.join(ROOT_PATH, "data/behavior_data")
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.mkdir(data_path)


if __name__ == '__main__':
    print("(O/N): Do you want to use pre-existing old data (O) or collect new data (N)?")
    user_answer = input()

    # If we are collecting new data
    if user_answer == 'N':
        purge_data_dir()

        # Record data for each of the six genomes
        for genome in GENOME_LIST:
            file_path = get_genome_file_path(genome)
            
            # Create a world with the genome
            sensors = SensorSet([BinaryLOSSensor(angle=0)])
            agent_config = DiffDriveAgentConfig(
                controller=genome.controller,
                sensors=sensors,
                seed=None
            )

            behavior = [metric.content(archiveMode=True) for metric in METRIC_LIST]

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
            for i in range(2000):
                world.step()

            # Metric data is stored in each behavior object
            # Write data to csv files to create a data archive
            with open(file_path, "a") as file:
                for i in range(len(METRIC_LIST)):
                    current_behavior = behavior[i]
                    filewriter = csv.writer(file, delimiter=',')
                    print(f"Writing data for the {current_behavior.name} behavior in the {genome.name} genome.")
                    filewriter.writerow([METRIC_LIST[i].name] + METRIC_LIST[i].content.get_archive(current_behavior))
            print("\n")


    # Processing the data, done regardless of user input
    for genome in GENOME_LIST:
        genome_name = genome.name
        file_path = get_genome_file_path(genome)
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            fig, ax = plt.subplots()
            ax.set_xlabel("Timesteps")
            ax.set_title(f"Behavior metrics over time for the \"{genome_name}\" genome")
            convergence_point = convergence_dict[genome_name]
            if convergence_point is not None:
                ax.axvline(convergence_point, color='red', linestyle='--')

            largest_y = None
            smallest_y = None
            data_length = None
            metric_name = None
            data = None

            for row in reader:
                metric_name = row[0]
                data = row[1:]
                data = [float(p) for p in data]
                data = convert_data_to_weighted_average(data, 25)

                # Update the upper and lower bounds of the graph
                smallest_y_in_series = min(data)
                largest_y_in_series = max(data)
                if largest_y is None and smallest_y is None:
                    largest_y = largest_y_in_series
                    smallest_y = smallest_y_in_series
                    data_length = len(data)
                if largest_y_in_series > largest_y:
                    largest_y = largest_y_in_series
                if smallest_y_in_series < smallest_y:
                    smallest_y = smallest_y_in_series

                line_color = line_color_dict[metric_name]
                ax.plot(data, label=metric_name, color=line_color, linewidth=2, linestyle='', marker='o', markersize=1)

            ax.legend(loc='upper right', bbox_to_anchor=(1.04, 1))
            ax.axis([0, data_length, smallest_y, largest_y])
            ax.set_ylim(smallest_y, largest_y)
            chartPath = get_genome_chart_path(genome)
            fig.tight_layout()
            fig.savefig(chartPath)

            