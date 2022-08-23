from src.novelty.NoveltyArchive import NoveltyArchive
from src.results.Trends import Trends


# define a main function
def main():
    archive = NoveltyArchive(from_file="trial_100_100_1661295094.csv")
    Trends().graphArchive(archive)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
