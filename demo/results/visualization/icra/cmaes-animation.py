import random
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas

CMAES_DATA_PATH = "../../out/LM-Mix-Fixed-1/n20-t4000-fixed/CMAES/genomes.csv"
# CMAES_DATA_PATH = "../../out/Homoge-Fixed-1/n20-t4000-fixed/CMAES/genomes.csv"
# CMAES_DATA_PATH = "../../out/Levy-Fixed-1/n20-t4000-fixed/CMAES/genomes.csv"
if __name__ == "__main__":
    data = pandas.read_csv(CMAES_DATA_PATH)
    comparisons = [
        # ["turning_rate_0", "forward_rate_0"],
        # ["turning_rate_1", "forward_rate_1"],
        # ["turning_rate", "forward_rate"],
        ["gen", "population_ratio"],
    ]

    # x0_range = tuple([-1.6, 1.6])
    # y0_range = tuple([-0.5, 10.5])

    x0_range = tuple([-5, 105])
    y0_range = tuple([-0.2, 1.2])

    fitness_vals = []

    def animate(gen):
        fig = plt.figure(constrained_layout=True, figsize=(10, 6))
        gs = GridSpec(2, 2, figure=fig)

        ax1 = fig.add_subplot(gs[0, :])
        # ax2 = fig.add_subplot(gs[1, 0])
        # ax3 = fig.add_subplot(gs[1, 1])
        # axs = [ax2, ax3]

        ax2 = fig.add_subplot(gs[1, :])
        axs = [ax2]

        df = data.loc[data["gen"] == gen]

        fitness_vals.append(max(df["Goal_Agents"]))

        if len(df) == 0:
            return

        """
        Fitness Over Time
        """
        ax1.set_title("Best Candidate Fitness (${P_g}$)")
        ax1.set_ylabel("Fitness (${P_g}$)")
        ax1.set_xlabel("Time (Generations)")
        ax1.plot([i for i in range(gen + 1)], fitness_vals)

        ax1.set_xlim(-1, 101)
        ax1.set_ylim(-0.05, 1.05)

        """
        CMA-ES
        """
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        for i, ax in enumerate(axs):
            # ax.set_title(f"Sensor On Controller (gen. {gen})" if i == 1 else f"Sensor Off Controller (gen. {gen})")
            # ax.set_title("Levy Controller")
            ax.set_title("Population Ratio Optimization")
            # ax.set_xlabel("Turning Rate (rad/s)")
            # ax.set_ylabel("Forward Rate (cm/s)")
            ax.set_xlabel("Generation")
            ax.set_ylabel("Population Ratio")
            ax.scatter(x=df[comparisons[i][0]], y=df[comparisons[i][1]], c=df["Goal_Agents"], cmap='plasma')
            ax.set_xlim(x0_range)
            ax.set_ylim(y0_range)

        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='plasma'), orientation='vertical', label='${P_g}$')
        plt.savefig(f"out/img-{gen}.png")
        plt.show()
        time.sleep(2.0)


    # plt.show()

    for gen in range(max(data["gen"])):
        animate(gen)