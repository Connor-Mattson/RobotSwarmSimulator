from src.novelty.NoveltyArchive import NoveltyArchive
from src.results.Trends import Trends
from src.results.Cluster import Cluster


# define a main function
def main():
    # archive = NoveltyArchive(
    #     pheno_file="trialA/pheno_100_100_1661362911.csv",
    #     geno_file="trialA/geno_100_100_1661362911.csv"
    # )

    archive = NoveltyArchive(
        pheno_file="trialD/pheno_g5_gen100_pop100_1661858162.csv",
        geno_file="trialD/geno_g5_gen100_pop100_1661858162.csv"
    )

    Trends().graphArchiveComparisons(archive)
    Trends().plotMetricHistograms(archive)

    clustering = Cluster(archive)
    clustering.displayGUI()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
