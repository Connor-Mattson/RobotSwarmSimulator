import math

import matplotlib.pyplot as plt
import numpy as np
import pandas

def standard_error(data):
    return np.std(data) / (math.sqrt(len(data)))

def gtz(x):
    return 1 if x > 0 else 0

def z_to_ten_k(x):
    return x if x > 0 else 10000

def success_rate_values(df, n_groups=30, key=None):
    success_rate = []
    snd_error = []
    for i in range(1, n_groups + 1):
        rows = df.loc[df["POPULATION_SIZE"] == i][key].to_numpy()
        mapped_vector = np.array(list(map(gtz, rows)))
        success_rate.append(mapped_vector.mean())
        snd_error.append(standard_error(mapped_vector))
    return range(1, n_groups + 1), success_rate, snd_error

def time_to_goal_values(df, n_groups=30, key=None):
    success_rate = []
    snd_error = []
    for i in range(1, n_groups + 1):
        values = df.loc[df["POPULATION_SIZE"] == i][key].to_numpy()
        values = np.array(list(map(z_to_ten_k, values)))
        success_rate.append(values.mean())
        snd_error.append(standard_error(values))
    return range(1, n_groups + 1), success_rate, snd_error

def levy_param_values(df, n_seeds=50, key=None):
    levy_values = []
    success_rate = []
    for i in range(1, n_seeds):
        rows = df.loc[df["SEED"] == i]
        levy_constant = rows.iloc[0]["LEVY_CONSTANT"]
        values = rows[key].to_numpy()
        values = np.array(list(map(gtz, values)))
        levy_values.append(levy_constant)
        success_rate.append(values.mean())
    return levy_values, success_rate


def plot_error_lines(data_tuple, name, xlabel, ylabel):
    for x, y, err, label in data_tuple:
        plt.errorbar(x, y, yerr=err, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(name)
    plt.legend()
    plt.show()

def plot_levy_success_values(levy_ds):
    x, y = levy_param_values(levy_ds, n_seeds=50, key="80_PERCENT")
    plt.scatter(x, y)
    plt.xlabel("Levy Parameter (Beta)")
    plt.ylabel("Success Rate")
    plt.title("Seeded Levy Constants")
    plt.show()

def plot_agent_success_rate(levy_ds, swarm_ds):
    # First Agent
    x1, y1, err1 = success_rate_values(levy_ds[["POPULATION_SIZE", "1_PERCENT"]], n_groups=29, key="1_PERCENT")
    x2, y2, err2 = success_rate_values(swarm_ds[["POPULATION_SIZE", "1_PERCENT"]], n_groups=29, key="1_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "At least one agent at goal", "No. Agents", "Success Rate (%)")

    # 25% of Agents to Goal
    x1, y1, err1 = success_rate_values(levy_ds[["POPULATION_SIZE", "25_PERCENT"]], n_groups=29, key="25_PERCENT")
    x2, y2, err2 = success_rate_values(swarm_ds[["POPULATION_SIZE", "25_PERCENT"]], n_groups=29, key="25_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "25% of agents at goal", "No. Agents", "Success Rate (%)")

    # 50% of Agents to Goal
    x1, y1, err1 = success_rate_values(levy_ds[["POPULATION_SIZE", "50_PERCENT"]], n_groups=29, key="50_PERCENT")
    x2, y2, err2 = success_rate_values(swarm_ds[["POPULATION_SIZE", "50_PERCENT"]], n_groups=29, key="50_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "50% of agents at goal", "No. Agents", "Success Rate (%)")

    # 80% of Agents to Goal
    x1, y1, err1 = success_rate_values(levy_ds[["POPULATION_SIZE", "80_PERCENT"]], n_groups=29, key="80_PERCENT")
    x2, y2, err2 = success_rate_values(swarm_ds[["POPULATION_SIZE", "80_PERCENT"]], n_groups=29, key="80_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "80% of agents to goal", "No. Agents", "Success Rate (%)")

    # 90% of Agents to Goal
    x1, y1, err1 = success_rate_values(levy_ds[["POPULATION_SIZE", "90_PERCENT"]], n_groups=29, key="90_PERCENT")
    x2, y2, err2 = success_rate_values(swarm_ds[["POPULATION_SIZE", "90_PERCENT"]], n_groups=29, key="90_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "90% of agents to goal", "No. Agents", "Success Rate (%)")

    # 100% of Agents to Goal
    x1, y1, err1 = success_rate_values(levy_ds[["POPULATION_SIZE", "100_PERCENT"]], n_groups=29, key="100_PERCENT")
    x2, y2, err2 = success_rate_values(swarm_ds[["POPULATION_SIZE", "100_PERCENT"]], n_groups=29, key="100_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "100% of agents to goal", "No. Agents", "Success Rate (%)")

def plot_time_to_goal(levy_ds, swarm_ds):
    # First Agent
    x1, y1, err1 = time_to_goal_values(levy_ds[["POPULATION_SIZE", "1_PERCENT"]], n_groups=29, key="1_PERCENT")
    x2, y2, err2 = time_to_goal_values(swarm_ds[["POPULATION_SIZE", "1_PERCENT"]], n_groups=29, key="1_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "At least one agent at goal", "No. Agents", "Time (timesteps)")

    # 25% of Agents to Goal
    x1, y1, err1 = time_to_goal_values(levy_ds[["POPULATION_SIZE", "25_PERCENT"]], n_groups=29, key="25_PERCENT")
    x2, y2, err2 = time_to_goal_values(swarm_ds[["POPULATION_SIZE", "25_PERCENT"]], n_groups=29, key="25_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "25% of agents at goal", "No. Agents", "Time (timesteps)")

    # 50% of Agents to Goal
    x1, y1, err1 = time_to_goal_values(levy_ds[["POPULATION_SIZE", "50_PERCENT"]], n_groups=29, key="50_PERCENT")
    x2, y2, err2 = time_to_goal_values(swarm_ds[["POPULATION_SIZE", "50_PERCENT"]], n_groups=29, key="50_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "50% of agents at goal", "No. Agents", "Time (timesteps)")

    # 80% of Agents to Goal
    x1, y1, err1 = time_to_goal_values(levy_ds[["POPULATION_SIZE", "80_PERCENT"]], n_groups=29, key="80_PERCENT")
    x2, y2, err2 = time_to_goal_values(swarm_ds[["POPULATION_SIZE", "80_PERCENT"]], n_groups=29, key="80_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "80% of agents to goal", "No. Agents", "Time (timesteps)")

    # 90% of Agents to Goal
    x1, y1, err1 = time_to_goal_values(levy_ds[["POPULATION_SIZE", "90_PERCENT"]], n_groups=29, key="90_PERCENT")
    x2, y2, err2 = time_to_goal_values(swarm_ds[["POPULATION_SIZE", "90_PERCENT"]], n_groups=29, key="90_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "90% of agents to goal", "No. Agents", "Time (timesteps)")

    # 100% of Agents to Goal
    x1, y1, err1 = time_to_goal_values(levy_ds[["POPULATION_SIZE", "100_PERCENT"]], n_groups=29, key="100_PERCENT")
    x2, y2, err2 = time_to_goal_values(swarm_ds[["POPULATION_SIZE", "100_PERCENT"]], n_groups=29, key="100_PERCENT")
    data = [(x1, y1, err1, "Levy Random Walk"), (x2, y2, err2, "Milling Controller")]
    plot_error_lines(data, "100% of agents to goal", "No. Agents", "Time (timesteps)")

if __name__ == "__main__":
    # Define Data Indices
    LEVY = {
        "_" : -1,
        "POPULATION_SIZE": 0,
        "SEED": 1,
        "LEVY_CONSTANT": 2,
        "WORLD_STEPS": 3,
        "DIST_TO_GOAL": 4,
        "AGENTS_AT_GOAL": 5,
        "1_PERCENT": 6,
        "10_PERCENT": 7,
        "25_PERCENT": 8,
        "50_PERCENT": 9,
        "80_PERCENT": 10,
        "90_PERCENT": 11,
        "95_PERCENT": 12,
        "100_PERCENT": 13
    }

    SWARMS = {
        "_" : -1,
        "POPULATION_SIZE": 0,
        "SEED": 1,
        "WORLD_STEPS": 2,
        "DIST_TO_GOAL": 3,
        "AGENTS_AT_GOAL": 4,
        "1_PERCENT": 5,
        "10_PERCENT": 6,
        "25_PERCENT": 7,
        "50_PERCENT": 8,
        "80_PERCENT": 9,
        "90_PERCENT": 10,
        "95_PERCENT": 11,
        "100_PERCENT": 12
    }

    # Import Data and set Column Attr Correctly
    levy_ds = pandas.read_csv("out/levy-solvers.csv")
    levy_ds.columns = list(LEVY.keys())

    swarm_ds = pandas.read_csv("out/swarm-solvers.csv")
    swarm_ds.columns = list(SWARMS.keys())

    # Plot Agents over Success Rate
    # plot_agent_success_rate(levy_ds, swarm_ds)

    # Plot Time to Goal
    # plot_time_to_goal(levy_ds, swarm_ds)

    # Plot Levy Parameter
    plot_levy_success_values(levy_ds)
