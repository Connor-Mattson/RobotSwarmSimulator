"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.defaults import ConfigurationDefaults
from novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from novel_swarms.results.results import main as report
from novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from novel_swarms.sensors.SensorSet import SensorSet

if __name__ == "__main__":

    sensors = SensorSet([
        # BinaryLOSSensor(angle=0),
        BinaryFOVSensor(theta=14 / 2, distance=300, degrees=True)
    ])

    agent_config = DiffDriveAgentConfig(
        agent_radius=5,
        dt=0.2,
        wheel_radius=(10 * 0.44),
        sensors=sensors,
        seed=None,
    )

    world_config = ConfigurationDefaults.RECTANGULAR_WORLD
    world_config.padding = 100
    world_config.population_size = 9
    world_config.addAgentConfig(agent_config)

    # Load the files into a novelty archive
    # Evolutionary archives are saved to files if GeneticEvolutionConfig.save_archive
    #   is set to True. Files can be found in /out,
    archive = NoveltyArchive(
        pheno_file="/home/connor/Desktop/SwarmSimulation/demo/evolution/out/b_1666819412_10_1666819486.csv",
        geno_file="/home/connor/Desktop/SwarmSimulation/demo/evolution/out/g_1666819412_10_1666819486.csv",
        absolute=True
    )

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Cluster and Explore Reduced Behavior Space
    report(config=results_config)
