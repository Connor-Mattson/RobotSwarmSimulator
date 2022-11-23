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

if __name__ == '__main__':
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
        # Metric data is archived in each behavior object

        simulate(world_config=world_config)
        
        for i in range(len(BEHAVIOR_LIST)):
            csvPath = os.path.join(BEHAVIOR_LIST[i].dirPath, "data.csv")
            with open(csvPath, "a") as file:
                filewriter = csv.writer(file, delimiter=',')
                print(f"Writing the {BEHAVIOR_LIST[i].name} data for the {genome.name} controller at {csvPath}.")
                filewriter.writerow([genome.name] + BEHAVIOR_LIST[i].content.get_archive(behavior[i]))
        
        print("\n")
    
    for behavior in BEHAVIOR_LIST:
        for genome in GENOME_LIST:
            csvPath = os.path.join(behavior.dirPath, "data.csv")
        

