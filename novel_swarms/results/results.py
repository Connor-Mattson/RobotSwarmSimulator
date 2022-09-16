from ..config.ResultsConfig import ResultsConfig
from .Cluster import Cluster
from .Trends import Trends


# define a main function
def main(config: ResultsConfig):
    if config.show_trends:
        Trends().graphArchiveComparisons(config.archive)
        Trends().plotMetricHistograms(config.archive)

    clustering = Cluster(config=config)
    clustering.displayGUI()
