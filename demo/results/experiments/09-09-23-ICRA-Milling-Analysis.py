import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(data_path):
    df = pd.read_csv(data_path)
    df["turning_radius_0"] = [min(abs(i / j), 250) for i, j in zip(df["forward_rate_0"], df["turning_rate_0"])]
    df["turning_radius_1"] = [min(abs(i / j), 250) for i, j in zip(df["forward_rate_1"], df["turning_rate_1"])]
    return df

def plot_evolution(data):
    x = data["time"]
    min_time = min(x)
    x = [elem - min_time for elem in x]
    y = data["Circliness"]
    plt.scatter(x, y, s=5)
    plt.title("Population Circliness during Evolutionary Optimization")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Circliness (Eq. 9)")
    plt.show()

def plot_evolution_over_generations(data):
    x = data["time"]
    min_time = min(x)

    x = range(1, 101)
    y = [np.mean(data.loc[data["gen"] == (i - 1)]["Circliness"]) for i in x]

    plt.plot(x, y)
    plt.title("Average Population Circliness during Evolutionary Optimization")
    plt.xlabel("Generation")
    plt.ylabel("Average Population Circliness (Eq. 9)")
    plt.show()

def plot_heatmap(data):
    ax = sns.relplot(
        data=data,
        x="turning_radius_0", y="turning_radius_1", hue="Circliness", size="Circliness",
        palette="vlag", hue_norm=(-1, 1), edgecolor=".7",
        height=10, sizes=(50, 250), size_norm=(-.2, .8),
    )
    plt.show()

if __name__ == "__main__":
    data = load_data("../out/ICRA_mill_optim_draft_1/CMAES/genomes.csv")
    plot_evolution_over_generations(data)