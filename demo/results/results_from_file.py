from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
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
    agent_config.body_color = (255,0,0)
    agent_config_2 = DiffDriveAgentConfig(
        sensors=sensors,
        body_color=(0, 255, 0)
    )
    hetero_config = HeterogeneousSwarmConfig()
    hetero_config.add_sub_populuation(agent_config, 12)
    hetero_config.add_sub_populuation(agent_config_2, 12)


    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=1,
        agentConfig=hetero_config,
        padding=15
    )

    # Load the files into a novelty archive
    # Evolutionary archives are saved to files if GeneticEvolutionConfig.save_archive
    #   is set to True. Files can be found in /out,
    archive = NoveltyArchive(
        pheno_file="/home/connor/Downloads/MRS_RESULTS/s1/NS6/NS6_s1_t1687461003_b__1687504387.csv",
        geno_file="/home/connor/Downloads/MRS_RESULTS/s1/NS6/NS6_s1_t1687461003_g__1687504387.csv",
        # pheno_file="/home/connor/Desktop/research/SwarmNoveltyNetwork/out/NS5_s0_t1686683208_b__1686697837.csv",
        # geno_file="/home/connor/Desktop/research/SwarmNoveltyNetwork/out/NS5_s0_t1686683208_g__1686697837.csv",
        # pheno_file="/home/connor/Desktop/research/SwarmNoveltyNetwork/src/z-experiments/MRS-notebooks/out/R-s0_repr_8__b_1687332766.csv",
        # geno_file="/home/connor/Desktop/research/SwarmNoveltyNetwork/src/z-experiments/MRS-notebooks/out/R-s0_repr_8__g_1687332766.csv",
        absolute=True
    )

    print(archive.archive.shape)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive
    results_config.early_exaggeration = 2
    results_config.perplexity = 20
    results_config.k = 20
    results_config.clustering_type = "hierarchical"
    # results_config.eps = 2.0

    # Cluster and Explore Reduced Behavior Space
    report(config=results_config, heterogeneous=True, dim_reduction=False)
