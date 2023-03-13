from ..config.ResultsConfig import ResultsConfig
from .Cluster import Cluster
from .Trends import Trends


# define a main function
def main(config: ResultsConfig, world_metadata=None):
    if config.show_trends:
        Trends().graphArchiveComparisons(config.archive)
        Trends().plotMetricHistograms(config.archive)

    clustering = Cluster(config=config, world_metadata=world_metadata)
    clustering.displayGUI()
