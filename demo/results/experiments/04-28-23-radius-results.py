import pandas
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_radii():
    radii = pandas.read_csv("out/cyclic-radii-exploration.csv", header=0, index_col=0)

    # combined_r = np.flip(df_sim_time.values, axis=0)
    # df_sim_time = pandas.DataFrame(combined_r)

    data = []
    for i, row in pandas.DataFrame(radii).iterrows():
        variance = row.loc["RADIAL_VARIANCE"]
        radius = row.loc["RADIUS"]
        if variance < 0.04:
            data.append([row.loc["CL0"], row.loc["CR0"], row.loc["CL1"], row.loc["CR1"], radius])
    data = np.array(data)

    x_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 2)]
    y_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 2)]
    z_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 2)]
    # y_tick_labels.reverse()

    fig = plt.figure(figsize=(10, 10))
    ax = Axes3D(fig)

    norm = matplotlib.colors.Normalize(vmin=min(data[:,4]), vmax=max(data[:,4]))
    cmap = cm.hot
    m = cm.ScalarMappable(norm=norm, cmap=cmap)

    CROSS_SECTION = 1.0
    new_data = []
    for d in data:
        if d[3] == 1.0:
            new_data.append(d)
    new_data = np.array(new_data)

    ax.scatter(new_data[:,0], new_data[:,1], new_data[:,2], c=m.to_rgba(new_data[:,4]), s=30)
    plt.colorbar(m)
    ax.set_xticklabels(x_tick_labels)
    ax.set_yticklabels(y_tick_labels)
    ax.set_zticklabels(z_tick_labels)
    ax.set_xlabel("$1$")
    ax.set_ylabel("$2$")
    ax.set_ylabel("$3$")
    plt.title("Radius of Cycle")
    plt.tight_layout()
    plt.show()

def plot_radii_v2():
    radii = pandas.read_csv("out/cyclic-radii-exploration-2.csv", header=0, index_col=0)

    data = []
    for i, row in pandas.DataFrame(radii).iterrows():
        variance = row.loc["RADIAL_VARIANCE"]
        radius = row.loc["RADIUS"]
        if variance < 0.0035:
            data.append([row.loc["CL0"], row.loc["CR0"], row.loc["CL1"], row.loc["CR1"], radius])
            if radius > 250:
                print(f"Radius: {radius}, row: {row}")
    data = np.array(data)

    norm = matplotlib.colors.Normalize(vmin=min(data[:, 4]), vmax=max(data[:, 4]))
    cmap = cm.plasma
    m = cm.ScalarMappable(norm=norm, cmap=cmap)

    new_data = []
    for d in data:
        v_r, v_l = d[2], d[3]
        v_on = (v_r + v_l) / 2
        dtheta_on = (v_r - v_l) / 7

        v_r, v_l = d[0], d[1]
        v_off = (v_r + v_l) / 2
        dtheta_off = (v_r - v_l) / 7

        pair = (dtheta_on, v_off)
        new_data.append([dtheta_on / dtheta_off, v_on / v_off, d[4]])
        # new_data.append([dtheta_on, dtheta_off, d[4]])
        # new_data.append([v_on, v_off, d[4]])
    new_data = np.array(new_data)
    print(f"Showing {len(new_data)} datapoints!")

    plt.scatter(new_data[:, 0], new_data[:, 1], c=m.to_rgba(new_data[:,2]), s=50)
    plt.colorbar(m)
    plt.xlabel("$theta_{on}:theta_{off}$")
    plt.ylabel("$v_{on}:v_{off}$")
    # plt.xlabel("$theta_{on}$")
    # plt.ylabel("$theta_{off}$")
    plt.title("Radius of Cyclic Pursuit Achieved Based off Control Inputs")
    plt.show()

def plot_radii_dist():
    radii = pandas.read_csv("out/cyclic-radii-exploration-2.csv", header=0, index_col=0)

    data = []
    for i, row in pandas.DataFrame(radii).iterrows():
        variance = row.loc["RADIAL_VARIANCE"]
        radius = row.loc["RADIUS"]
        if variance < 0.003:
            data.append([row.loc["CL0"], row.loc["CR0"], row.loc["CL1"], row.loc["CR1"], radius])
            if radius > 250:
                print(f"Radius: {radius}, row: {row}")
    data = np.array(data)

    plt.hist(data[:,4], bins=20, density=True)
    plt.xlabel("Pursuit radius")
    plt.ylabel("Probability")
    # plt.xlabel("$theta_{on}$")
    # plt.ylabel("$theta_{off}$")
    plt.title("Radius of Cyclic Pursuit Achieved Based off Control Inputs")
    plt.show()

if __name__ == "__main__":
    plot_radii_v2()