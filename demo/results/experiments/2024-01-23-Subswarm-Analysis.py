import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm

def load_data(path):
    return pd.read_csv(path)

def get_mean_std(df):
    df = df.loc[df["subswarms"] > 1]
    target_attr = "time"
    x, y, mu, sigma = [], [], [], []
    for n in range(10, 23, 1):
        phi_above_manifold = [phi if phi > (360 / n) else None for phi in range(3, 76, 1)]
        final_phi = list(filter(lambda x: x is not None, phi_above_manifold))
        for phi in final_phi:
            ds = df.loc[df["n"] == n]
            ds = ds.loc[ds["fov"] == phi]
            if len(ds) == 0:
                print(f"Specified n={n}, fov={phi} do not exist in the dataset")
                continue
            target_col = ds[target_attr].to_numpy()
            mean, std = np.mean(target_col), np.std(target_col)
            x.append(n)
            y.append(phi)
            mu.append(mean)
            sigma.append(std)
    return x, y, mu, sigma

def get_mean_std_dt_trials(df):
    target_attr = "max_sub_pop"
    x, y, mu, sigma = [], [], [], []
    for dt in [i / 100 for i in range(4, 14, 2)]:
        for phi in range(26, 40, 3):
            ds = df.loc[df["dt"] == dt]
            ds = ds.loc[ds["fov"] == phi]
            if len(ds) == 0:
                raise Exception(f"Specified dt={dt}, fov={phi} do not exist in the dataset")
            target_col = ds[target_attr].to_numpy()
            mean, std = np.mean(target_col), np.var(target_col)
            x.append(dt)
            y.append(phi)
            mu.append(mean)
            sigma.append(std)
    return x, y, mu, sigma

def plot_mean_std(n, phi, mu, sigma):
    # f, ax = plt.subplots(4, 1, sharex=True, sharey=True)
    # i = 0
    # for target_n in range(15, 23, 2):
    #     x_fov = []
    #     y_mean = []
    #     y_error = []
    #     for N, fov, mean, std in zip(n, phi, mu, sigma):
    #         if N == target_n:
    #             x_fov.append(fov)
    #             y_mean.append(mean)
    #             y_error.append(std / np.sqrt(20))
    #     ax[i].plot(x_fov, y_mean, label=f"N={target_n}")
    #     ax[i].axvline(x=360 / target_n, color='r')
    #     ax[i].fill_between(x_fov, np.array(y_mean) - np.array(y_error), np.array(y_mean) + np.array(y_error), alpha=0.2)
    #     ax[i].set_title(f"{target_n} Agents")
    #     i += 1

    # plt.xlabel("$\phi$ (degrees)")
    # # f.legend()
    # # f.set_ylabel("Average No. Subswarms over 20 seeds")
    # # f.set_title("No. Emergent Subswarms for N agents with FOV $\phi$")
    # plt.show()

    # for target_phi in range(30, 76, 10):
    #     x_n = []
    #     y_mean = []
    #     for N, fov, mean, var in zip(n, phi, mu, sigma):
    #         if fov == target_phi:
    #             x_n.append(N)
    #             y_mean.append(mean)
    #     plt.plot(x_n, y_mean, label=f"$\phi={target_phi}$")
    # plt.xlabel("No. Agents (N)")
    # plt.ylabel("Average No. Subswarms over 20 seeds")
    # plt.title("Avg. No. Subswarms formed for N Agents")
    # plt.legend()
    # plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(n, phi, mu, marker='o', c=mu, cmap=cm.viridis)
    ax.set_xlabel("N Agents")
    ax.set_ylabel("$\phi$")
    ax.set_zlabel("Avg. Decomposition Time (s)")
    plt.title("Time from Initialization to Full Decomposition")
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(n, phi, sigma, marker='o', c=sigma, cmap=cm.viridis)
    ax.set_xlabel("N Agents")
    ax.set_ylabel("$\phi$")
    ax.set_zlabel("Decomposition Time Var.")
    plt.title("Decomposition Time for Swarms above Manifold")
    plt.show()

def plot_mean_std_dt_trials(dt, phi, mu, sigma):
    # f, ax = plt.subplots(4, 1, sharex=True, sharey=True)
    # i = 0
    # for target_n in range(15, 23, 2):
    #     x_fov = []
    #     y_mean = []
    #     y_error = []
    #     for N, fov, mean, std in zip(n, phi, mu, sigma):
    #         if N == target_n:
    #             x_fov.append(fov)
    #             y_mean.append(mean)
    #             y_error.append(std / np.sqrt(20))
    #     ax[i].plot(x_fov, y_mean, label=f"N={target_n}")
    #     ax[i].axvline(x=360 / target_n, color='r')
    #     ax[i].fill_between(x_fov, np.array(y_mean) - np.array(y_error), np.array(y_mean) + np.array(y_error), alpha=0.2)
    #     ax[i].set_title(f"{target_n} Agents")
    #     i += 1

    # plt.xlabel("$\phi$ (degrees)")
    # # f.legend()
    # # f.set_ylabel("Average No. Subswarms over 20 seeds")
    # # f.set_title("No. Emergent Subswarms for N agents with FOV $\phi$")
    # plt.show()

    # for target_phi in range(30, 76, 10):
    #     x_n = []
    #     y_mean = []
    #     for N, fov, mean, var in zip(n, phi, mu, sigma):
    #         if fov == target_phi:
    #             x_n.append(N)
    #             y_mean.append(mean)
    #     plt.plot(x_n, y_mean, label=f"$\phi={target_phi}$")
    # plt.xlabel("No. Agents (N)")
    # plt.ylabel("Average No. Subswarms over 20 seeds")
    # plt.title("Avg. No. Subswarms formed for N Agents")
    # plt.legend()
    # plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(dt, phi, mu, marker='o', c=mu, cmap=cm.viridis)
    ax.set_xlabel("dt (s)")
    ax.set_ylabel("$\phi$")
    ax.set_zlabel("Avg. no. Subswarms")
    plt.title("Avg. No. Subswarms after Decomposition as dt increases (N=16)")
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(dt, phi, sigma, marker='o', c=sigma, cmap=cm.viridis)
    ax.set_xlabel("dt (s)")
    ax.set_ylabel("$\phi$")
    ax.set_zlabel("Largest Subswarm Size Variance.")
    plt.title("Largest Subswarm Size Variance as dt increases (N=16)")
    plt.show()

def rewrite_data_out(df):
    actual_dts = [i / 100 for i in range(4, 14, 2)]
    col = []
    for dt in actual_dts:
        col += [dt] * 120
    df.insert(2, "dt", col, False)
    df = df.loc[df["subswarms"] > 1]
    df.to_csv("../out/subswarm-dt/sweep/genes-with-dt.csv")


if __name__ == "__main__":
    df = load_data("../out/subswarm/sweep/genes.csv")
    n, phi, mu, sigma = get_mean_std(df)
    plot_mean_std(n, phi, mu, sigma)

    # df = pd.read_csv("../out/subswarm-dt/sweep/genes-with-dt.csv")
    # dt, phi, mu, sigma = get_mean_std_dt_trials(df)
    # plot_mean_std_dt_trials(dt, phi, mu, sigma)
