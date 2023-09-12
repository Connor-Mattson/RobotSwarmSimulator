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


def aggregate_data(data, file_name="results.tsv"):
    """
    Convert to GMU format (Kevin)
    """
    res = [[None, 0, repr([])]]
    for i in range(100):
        print(i)
        time = data.loc[data["gen"] == i].head(1)["time"].item()
        epoch = i + 1
        fitness = list(data.loc[data["gen"] == i]["Circliness"])
        l = [time, epoch, repr(fitness)]
        res.append(l)
    df = pd.DataFrame(res, columns=["time", "epoch", "fitness"])
    df.to_csv(file_name, sep="\t", index=False)
    print("Completed!")

def load_tsv_file(path):
    import csv
    out = []
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            out.append(row)
    return out

def plot_compare_with_kevin():
    KEVIN_FILE = "Kevin_1000t_n10_p50.tsv"
    CONNOR_FILE = "Connor_P50_T1000_N10.tsv"
    K_dat = load_tsv_file(KEVIN_FILE)
    C_dat = load_tsv_file(CONNOR_FILE)

    DATA = [K_dat, C_dat]
    LABEL = ["SNN", "Symbolic"]
    COLORS = ["red", "blue"]
    SHAPE = ["*", "^"]
    fig, ax = plt.subplots()
    for d, l, c, s in zip(DATA, LABEL, COLORS, SHAPE):
        time_start = float(d[0][0])
        x = []
        y = []
        for i in range(len(d)):
            fitnesses = eval(d[i][2])
            for f in fitnesses:
                # x.append(float(d[i][0]) - time_start)
                x.append(i)
                y.append(f)
        ax.scatter(x, y, c=c, s=2, label=l, alpha=0.8)
    ax.legend(loc='upper right')
    # plt.xlabel("Time (seconds)")
    plt.xlabel("Epochs")
    plt.ylabel("Circliness (Eq. 9)")
    plt.title("Population Circliness Distribution during G.A.")
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
    # data = load_data("../out/comp_w_kevin/CMAES/genomes.csv")
    # aggregate_data(data, "P50_T1000_N10.tsv")
    plot_compare_with_kevin()
