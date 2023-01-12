from novel_swarms.config.defaults import ConfigurationDefaults
from novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from sklearn.manifold import TSNE
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
        pheno_file="/home/connor/Desktop/Experiments/Daily-Trials/01-12-23-mutation/b_1673543323_final_1673544117.csv",
        geno_file="/home/connor/Desktop/Experiments/Daily-Trials/01-12-23-mutation/g_1673543323_final_1673544117.csv",
        absolute=True
    )

    CONTROLLER_MAX = 750
    BEHAVIOR_MAX = 750
    CRAWL_STRIDE = 16
    FRAMES = CONTROLLER_MAX // CRAWL_STRIDE

    controllers = archive.genotypes[:min(CONTROLLER_MAX, len(archive.genotypes))]
    behaviors = archive.archive[:min(BEHAVIOR_MAX, len(archive.archive))]

    # Reduce dimensions for both the controllers and the behaviors
    print("Reducing Controllers...")
    controllers_reduced = TSNE(
        n_components=2,
        learning_rate="auto",
        init="pca",
        perplexity=25,
        early_exaggeration=1
    ).fit_transform(controllers)

    print("Reducing Behaviors...")
    behaviors_reduced = TSNE(
        n_components=2,
        learning_rate="auto",
        init="pca",
        perplexity=25,
        early_exaggeration=1
    ).fit_transform(behaviors)

    # Calculate the boundaries for the output frames
    C_PADDING, B_PADDING = 12, 6
    max_controllers_x, max_controllers_y = max(controllers_reduced[:,0]), max(controllers_reduced[:, 1])
    min_controllers_x, min_controllers_y = min(controllers_reduced[:, 0]), min(controllers_reduced[:, 1])
    max_behaviors_x, max_behaviors_y = max(behaviors_reduced[:, 0]), max(behaviors_reduced[:, 1])
    min_behaviors_x, min_behaviors_y = min(behaviors_reduced[:, 0]), min(behaviors_reduced[:, 1])

    heat = [(i // CRAWL_STRIDE) for i in range(0, CONTROLLER_MAX)]
    print(heat)

    for i in range(1, FRAMES + 1):
        seen_controllers = controllers_reduced[:(i * CRAWL_STRIDE)]
        seen_behaviors = behaviors_reduced[:(i * CRAWL_STRIDE)]
        colors = heat[:(i * CRAWL_STRIDE)]

        fig = plt.figure(figsize=(18, 9))
        rows = 1
        columns = 2

        fig.add_subplot(rows, columns, 1)
        plt.xlim(min_controllers_x - C_PADDING, max_controllers_x + C_PADDING)
        plt.ylim(min_controllers_y - C_PADDING, max_controllers_y + C_PADDING)
        plt.scatter(seen_controllers[:,0], seen_controllers[:,1], c=colors, cmap="plasma", vmax=max(colors), vmin=min(colors))
        plt.title(f"Controller Space Exploration (Generation {i})")
        plt.xlabel("T-SNE X-Reduction")
        plt.ylabel("T-SNE Y-Reduction")

        fig.add_subplot(rows, columns, 2)
        plt.xlim(min_behaviors_x - B_PADDING, max_behaviors_x + B_PADDING)
        plt.ylim(min_behaviors_y - B_PADDING, max_behaviors_y + B_PADDING)
        plt.scatter(seen_behaviors[:, 0], seen_behaviors[:, 1], c=colors, cmap="plasma", vmax=max(colors), vmin=min(colors))
        plt.title(f"Behavior Space Exploration (Generation {i})")
        plt.xlabel("T-SNE X-Reduction")
        plt.ylabel("T-SNE Y-Reduction")

        # plt.show()
        F_OUT = f"out/gen-{i}.png"
        plt.savefig(F_OUT)
