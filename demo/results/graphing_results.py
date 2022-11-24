# READ BEFORE RUNNING
# This file must be run from the top level of the project
# The `total_allowed_steps` variable in simulate.py must not be `None`
# Change `total_allowed_steps` back to `None` after running this file
# I know it's hacky, but it works for now

from novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from novel_swarms.behavior.Squareness import SquarenessBehavior
from novel_swarms.behavior.KNN import KNNBehavior
from novel_swarms.behavior.MeanNeighbors import MeanNeighborDistance
from novel_swarms.behavior.LargestSeparation import LargestSeparationBehavior

from novel_swarms.world.simulate import main as simulate
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig

import os
import shutil
from collections import namedtuple
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

Genome = namedtuple("Genome", "name controller")
Behavior = namedtuple("Behavior", "name content dirPath")

GENOME_LIST = [
    Genome('aggregation', [-0.7, -1.0, 1.0, -1.0]),
    Genome('entropic', [-0.83, -0.75, 0.27, -0.57]),
    Genome('wall-following', [1.0, 0.98, 1.0, 1.0]),
    Genome('cyclic-pursuit', [-0.7, 0.3, 1.0, 1.0]),
    Genome('dispersal', [0.2, 0.7, -0.5, -0.1]),
    Genome('milling', [-0.69, -0.77, 0.05, -0.4])
    ]

BEHAVIOR_LIST = [
    Behavior('angular-momentum', AngularMomentumBehavior, os.path.join("data/behavior_data/" + 'angular-momentum')),
    Behavior('average-speed', AverageSpeedBehavior, os.path.join("data/behavior_data/" + 'average-speed')),
    Behavior('group-rotation', GroupRotationBehavior, os.path.join("data/behavior_data/" + 'group-rotation')),
    Behavior('radial-variance', RadialVarianceBehavior, os.path.join("data/behavior_data/" + 'radial-variance')),
    Behavior('scatter', ScatterBehavior, os.path.join("data/behavior_data/" + 'scatter')),
    Behavior('squareness', SquarenessBehavior, os.path.join("data/behavior_data/" + 'squareness')),
    Behavior('knn', KNNBehavior, os.path.join("data/behavior_data/" + 'knn')),
    Behavior('neighbor-dist', MeanNeighborDistance, os.path.join("data/behavior_data/" + 'neighbor-dist')),
    Behavior('largest-separation', LargestSeparationBehavior, os.path.join("data/behavior_data/" + 'largest-separation'))
]

def get_behavior_dir_path(behavior):
    return os.path.join("data/behavior_data/" + behavior.name)

if __name__ == '__main__':
    print("(O/N): Do you want to use pre-existing old data (O) or collect new data (N)?")
    user_answer = input()

    # If we are collecting new data
    if user_answer == 'N':
        # Clear all previous data
        shutil.rmtree("data/behavior_data/", ignore_errors=False)
        os.mkdir("data/behavior_data/")

        # In the behavior_data directory, make a sub-directory to record data on each behavior
        for behavior in BEHAVIOR_LIST:
            os.mkdir(behavior.dirPath)

        # Record data for each of the six genomes
        for genome in GENOME_LIST:
            # Create a world with the genome
            SEED = None
            sensors = SensorSet([BinaryLOSSensor(angle=0)])
            agent_config = DiffDriveAgentConfig(
                controller=genome.controller,
                sensors=sensors,
                seed=SEED
            )
            behavior = [behavior.content(archiveMode=True) for behavior in BEHAVIOR_LIST]
            world_config = RectangularWorldConfig(
                size=(500, 500),
                n_agents=30,
                seed=SEED,
                behavior=behavior,
                agentConfig=agent_config,
                padding=15
            )

            # Simulate the world with the genome
            # All metrics are tracked until the world is exited

            simulate(world_config=world_config)
            
            # Metric data is stored in each behavior object
            # Write data to csv files to create a data archive
            for i in range(len(BEHAVIOR_LIST)):
                csvPath = os.path.join(BEHAVIOR_LIST[i].dirPath, "data.csv")
                with open(csvPath, "a") as file:
                    filewriter = csv.writer(file, delimiter=',')
                    print(f"Writing the {BEHAVIOR_LIST[i].name} data for the {genome.name} controller at {csvPath}.")
                    filewriter.writerow([genome.name] + BEHAVIOR_LIST[i].content.get_archive(behavior[i]))
            
            print("\n")
    
    convergence_dict = {
        'aggregation': 450,
        'entropic': None,
        'wall-following': 260,
        'cyclic-pursuit': 650,
        'dispersal': 320,
        'milling': None
    }
    # Processing the data, done regardless of user input
    for behavior in BEHAVIOR_LIST:
        csvPath = os.path.join(behavior.dirPath, "data.csv")
        with open(csvPath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                genome_name = row[0]
                data = row[1:]
                data = [float(p) for p in data]
                fig, ax = plt.subplots()
                ax.plot(data, color='orange', linewidth=2, linestyle='', marker='o', markersize=1)

                ax.set_xlabel("Timesteps")
                ax.set_ylabel(behavior.name)
                ax.set_title(f"{behavior.name} over time for the \"{genome_name}\" genome")
                ax.axis([0, len(data), min(data), max(data)])
                ax.set_ylim(min(data), max(data))
                fig.tight_layout()
                convergence_point = convergence_dict[genome_name]
                if convergence_point is not None:
                    ax.axvline(convergence_point, color='red', linestyle='--')
                chartPath = os.path.join(behavior.dirPath, genome_name)
                fig.savefig(chartPath)

            