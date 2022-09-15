from src.novelty.NoveltyArchive import NoveltyArchive
from src.results.Trends import Trends
from src.results.Cluster import Cluster
from src.config.WorldConfig import RectangularWorldConfig
from src.config.ResultsConfig import ResultsConfig


# define a main function
def main(config: ResultsConfig):
    if config.show_trends:
        Trends().graphArchiveComparisons(config.archive)
        Trends().plotMetricHistograms(config.archive)

    clustering = Cluster(config=config)
    clustering.displayGUI()
