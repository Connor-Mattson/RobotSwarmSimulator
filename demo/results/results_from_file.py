"""
Feel free to copy this file and explore configurations that lead to interesting results.

If you do not plan to make commits to the GitHub repository or if you can ensure that changes to this file
are not included in your commits, you may directly edit and run this file.

Connor Mattson
University of Utah
September 2022
"""
from novel_swarms.config.defaults import ConfigurationDefaults
from novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from novel_swarms.results.results import main as report

if __name__ == "__main__":

    agent_config = ConfigurationDefaults.FOV_DIFF_DRIVE_AGENT
    world_config = ConfigurationDefaults.RECTANGULAR_WORLD
    world_config.addAgentConfig(agent_config)

    # Load the files into a novelty archive
    # Evolutionary archives are saved to files if GeneticEvolutionConfig.save_archive
    #   is set to True. Files can be found in /out,
    archive = NoveltyArchive(
        pheno_file="GMU/GMUpheno.csv",
        geno_file="GMU/GMUgenome.csv"
    )

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Cluster and Explore Reduced Behavior Space
    report(config=results_config)
