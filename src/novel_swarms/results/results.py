from ..config.ResultsConfig import ResultsConfig
from ..results.Cluster import Cluster
from ..results.Trends import Trends


# define a main function
def main(config: ResultsConfig, world_metadata=None, heterogeneous=False, dim_reduction=False):
    if config.show_trends:
        Trends().graphArchiveComparisons(config.archive)
        Trends().plotMetricHistograms(config.archive)

    clustering = Cluster(config=config, world_metadata=world_metadata, heterogeneous=heterogeneous, dim_reduction=False)
    clustering.displayGUI()
