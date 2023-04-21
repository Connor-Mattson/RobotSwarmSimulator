import numpy as np
from matplotlib import pyplot, colors
from matplotlib.patches import Patch

from novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from novel_swarms.results.Trends import Trends
from novel_swarms.world.RectangularWorld import RectangularWorld

NUM_STATS = 4

def getDummyDist():
    dist = [[0.0 for j in range(NUM_STATS)] for i in range(len(5))]
    return dist


def getDistributionStats(behavior):
    dist = np.array([[0.0 for j in range(NUM_STATS)] for i in range(len(behavior[0]))])
    for i in range(len(behavior[0])):
        metrics = behavior[:, i]
        _range = max(metrics) - min(metrics)
        q3, q1 = np.percentile(metrics, [75, 25])
        iqr = q3 - q1
        std = np.std(metrics)
        variance = np.var(metrics)
        dist[i] = [_range, iqr, std, variance]

    return dist


def main():
    DENSITY = 20
    TRIALS = 5
    SAMPLE_SIZE = 20

    r_0_s = np.linspace(-1.0, 1.0, num=DENSITY)
    r_1_s = np.linspace(-1.0, 1.0, num=DENSITY)
    l_0_s = np.linspace(-1.0, 1.0, num=DENSITY)
    l_1_s = np.linspace(-1.0, 1.0, num=DENSITY)

    mesh = np.meshgrid(r_0_s, l_0_s, r_1_s, l_1_s)
    genomes = np.array(mesh).T.reshape(-1, 4)

    index_sample = np.random.randint(len(genomes), size=SAMPLE_SIZE)
    genome_sample = np.array([genomes[i] for i in index_sample])

    # Behaviors at t {behavior_timestep}
    timesteps = [300 * i for i in range(1, 10)]
    populations = [i for i in range(10, 30, 2)]

    # Test
    # timesteps = [10, 20, 30, 40, 50, 60, 70]
    # populations = [40, 50, 60, 70]

    # Test - Lower Space
    # timesteps = [50, 100, 150]
    # populations = [10, 20, 30]

    # Test - Higher Space
    # timesteps = [200, 250, 300]
    # populations = [40, 50, 60]

    # Test - Both High and Low Space
    # timesteps = [50, 100, 150, 200, 250, 300]
    # populations = [10, 20, 30, 40, 50, 60]

    # Any Values
    # timesteps = [1, 2, 3, 4, 5]
    # populations = [2, 3]

    behavior_dist_metrics = np.zeros((len(timesteps), len(populations), 5, NUM_STATS))

    print(f"Size of Genome scope: {len(genomes)}")
    print("Creating Data...")
    for i, pop_size in enumerate(populations):
        print(f"Running World with population {pop_size}...")

        for trial in range(TRIALS):
            print(f"p{pop_size}_trial{trial}")
            behavior = [None for _ in range(len(timesteps))]
            for j, gene in enumerate(genome_sample):
                world = RectangularWorld(
                    w=500, h=500,
                    pop_size=pop_size,
                )
                world.setup(controller=gene, seed=trial)
                for step in range(max(timesteps) + 1):
                    world.step()
                    if step in timesteps:
                        index = timesteps.index(step)
                        if behavior[index] is None:
                            behavior[index] = np.array([world.getBehaviorVector()])
                        else:
                            behavior[index] = np.concatenate((behavior[index], [world.getBehaviorVector()]))

            for j, behav in enumerate(behavior):
                my_stats = getDistributionStats(behav)
                behavior_dist_metrics[j][i] += my_stats

        for j in range(len(timesteps)):
            behavior_dist_metrics[j][i] /= TRIALS  # Average Statistics over the trials

    stats_labels = ["Range", "IQR", "Standard Deviation", "Variance"]
    behavior_labels = ["Average Speed", "Angular Momentum", "Radial Variance", "Scatter", "Group Rotation"]
    for i in range(len(behavior_dist_metrics[0][0])):
        for l in range(len(stats_labels)):
            data = np.array(
                [[behavior_dist_metrics[j][k][i][l] for k in range(len(populations))] for j in range(len(timesteps))])
            pyplot.figure()
            pyplot.title(f"{behavior_labels[i]} - {stats_labels[l]}")
            pyplot.ylabel("Time in Environment (timesteps)")
            pyplot.xlabel("Number of Agents")
            pyplot.yticks(range(0, len(timesteps)), timesteps[::-1])
            pyplot.xticks(range(0, len(populations)), populations)

            colormap = colors.ListedColormap(["darkblue", "royalblue", "lightsteelblue", "aliceblue", "ghostwhite"])

            pyplot.margins(x=10)

            zdata = data.ravel()
            # pcm = pyplot.pcolor(populations, timesteps, data,
            #                     norm=colors.LogNorm(vmin=min(zdata), vmax=max(zdata)),
            #                     cmap='YlGn')

            im = pyplot.imshow(data[::-1], interpolation="bilinear")
            pyplot.colorbar(im, extend='max')
            pyplot.show()

            # print(f"{behavior_labels[i]} - {stats_labels[l]} \n BL: {data[0][0]}, BR: {data[0][-1]}, TR: {data[-1][-1]}, TL: {data[-1][0]}")

    print("DONE!")


if __name__ == "__main__":
    main()
