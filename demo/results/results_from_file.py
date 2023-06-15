from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from src.novel_swarms.results.results import main as report
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet

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
        pheno_file="/home/jeremy/Documents/RobotSwarmSimulator/data/NS5_s0_t1686683208_b__1686697837.csv",
        geno_file="/home/jeremy/Documents/RobotSwarmSimulator/data/NS5_s0_t1686683208_g__1686697837.csv",
        absolute=True
    )

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive
    results_config.clustering_type = "dbscan"
    results_config.k = 6

    # Cluster and Explore Reduced Behavior Space
    report(config=results_config)
