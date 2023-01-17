from novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from sklearn.manifold import TSNE
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

if __name__ == "__main__":
    # Load the files into a novelty archive
    # Evolutionary archives are saved to files if GeneticEvolutionConfig.save_archive
    #   is set to True. Files can be found in /out,
    archive = NoveltyArchive(
        # pheno_file="/home/connor/Desktop/Experiments/Daily-Trials/01-11-23-heuristic-evolution/b_1673482837_final_1673485568.csv",
        # geno_file="/home/connor/Desktop/Experiments/Daily-Trials/01-11-23-heuristic-evolution/g_1673482837_final_1673485568.csv",
        absolute=True
    )

    GENERATIONS = 50
    POPULATION = len(archive.archive) // GENERATIONS

    novelty_scores = []
    archive_2 = NoveltyArchive()
    for GEN in range(1, GENERATIONS):
        archive_2.archive = archive.archive[:(GEN * POPULATION)]
        gen_scores = []
        for POP in range(POPULATION):
            n = archive_2.getNovelty(15, archive.archive[(GEN * POPULATION) + POP])
            gen_scores.append(n)
        novelty_scores.append(np.average(gen_scores))
        print(f"Generation {GEN}: {np.average(gen_scores)}")

    print(novelty_scores)