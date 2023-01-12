"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.config.defaults import ConfigurationDefaults
from novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from novel_swarms.results.results import main as report
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.SensorSet import SensorSet

if __name__ == "__main__":

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
        # BinaryLOSSensor(angle=45),
        # BinaryLOSSensor(angle=45)
        # BinaryFOVSensor(theta=14 / 2, distance=(20 * 13.25), degrees=True)
    ])

    agent_config = ConfigurationDefaults.DIFF_DRIVE_AGENT

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=1,
        agentConfig=agent_config,
        padding=15
    )

    # Load the files into a novelty archive
    # Evolutionary archives are saved to files if GeneticEvolutionConfig.save_archive
    #   is set to True. Files can be found in /out,
    archive = NoveltyArchive(
        pheno_file="/home/connor/Desktop/Experiments/Daily-Trials/01-09-23-seeded/b_1673303183_final_1673306585.csv",
        geno_file="/home/connor/Desktop/Experiments/Daily-Trials/01-09-23-seeded/g_1673303183_final_1673306585.csv",
        absolute=True
    )

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Cluster and Explore Reduced Behavior Space
    report(config=results_config)
