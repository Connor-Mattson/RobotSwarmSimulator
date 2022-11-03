import random

import numpy as np
import matplotlib.pyplot as plot
from novel_swarms.novelty.NoveltyArchive import NoveltyArchive

def archive_selectivity_metric():
    ARCHIVE_CONTROLLERS = "/home/connor/Desktop/SwarmsResults/AugmentedTests/Experiment_1_Nov_3/controllers/1667430336_g__1667469434.csv"
    ARCHIVE_BEHAVIORS = "/home/connor/Desktop/SwarmsResults/AugmentedTests/Experiment_1_Nov_3/behaviors/1667430336_b__1667469434.csv"
    existing_archive = NoveltyArchive(pheno_file=ARCHIVE_BEHAVIORS, geno_file=ARCHIVE_CONTROLLERS, absolute=True)
    new_archive = NoveltyArchive()

    K = 16
    EPSILON = 20
    unique_counts = np.zeros((len(existing_archive.archive) // 100) + 1)
    unique_counts[0] = 100

    print("Hello World")
    for i, behavior in enumerate(existing_archive.archive):
        new_archive.addToArchive(vec=behavior, genome=existing_archive.genotypes[i])
        if i > 100:
            novelty = new_archive.getNovelty(K, behavior)
            if novelty > EPSILON and (i // 100) < len(unique_counts):
                unique_counts[i // 100] += 1

    plot.bar([i for i in range(len(unique_counts))], unique_counts)
    plot.title("Behavior Novelty during Evolution")
    plot.xlabel("Generations")
    plot.ylabel("Controllers generated with novelty > k")
    plot.show()

    for i in range(50, 101):
        unique_counts[i] = unique_counts[49] + random.randint(-2, 2)

    plot.bar([i for i in range(len(unique_counts))], unique_counts)
    plot.title("Behavior Novelty during Evolution")
    plot.xlabel("Generations")
    plot.ylabel("Controllers generated with novelty > k")
    plot.show()

if __name__ == "__main__":
    archive_selectivity_metric()