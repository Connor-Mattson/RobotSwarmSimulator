"""
Find the best Homogeneous Agents
"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import LinearLocator
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib
from pylab import cm

# RESULTS_FILE = "../../../demo/results/out/SM-1700086019/sweep/genes.csv"
RESULTS_FILE = "../../../demo/results/out/SM-Full-Run/sweep/genes.csv"

def plot_lambda_2(df):
    # Filter lambda 2
    # l2 = df.loc["lambda_2" == 0]
    # hm_pre = df.assign(threshold=df['lambda_2_500'] == 1)
    hm = df.pivot(index="fov", columns="n", values="lambda_2_500")
    sns.heatmap(hm[::-1], cmap="crest")
    plt.title("$\lambda_2$ in Laplacian (Average over final 500 timesteps)")
    plt.xlabel("N")
    plt.ylabel("$\phi$")
    plt.show()

def plot_cc(df):
    # Filter lambda 2
    # l2 = df.loc["lambda_2" == 0]
    # hm_pre = df.assign(threshold=df['lambda_2_500'] == 1)
    hm = df.pivot(index="fov", columns="n", values="conn_components")
    sns.heatmap(hm[::-1], cmap="crest")
    plt.title("No. Connected Components")
    plt.xlabel("N")
    plt.ylabel("$\phi$")
    plt.show()

def plot_circliness(df):
    hm = df.pivot(index="fov", columns="n", values="radial_variance")
    sns.heatmap(hm[::-1], cmap="crest")
    plt.title("Radial Variance")
    plt.xlabel("N")
    plt.ylabel("$\phi$")
    plt.show()

def plot_radius(df):
    # df = df.loc[df["conn_components"] <= 1]
    df = df.loc[df["fov"] == 45]
    # df = df.loc[df["omega"] == 20]
    df = df.loc[df["lambda_2_500"] == 1.0]
    hm = df.pivot(index="v", columns="omega", values="lambda_2")
    sns.heatmap(hm[::-1], cmap="crest")
    plt.title("Mill Radius (cm)")
    plt.xlabel("V")
    plt.ylabel("$\phi$")
    plt.show()

def cluster_and_report(df):

    # df = df.loc[(df["n"] < 14) | (df["fov"] <= 27)]
    df = df.loc[df["lambda_2"] == 1.0]
    X = df.loc[:, "average_speed":"group_rotation"]
    print(X.shape)
    af = KMeans(n_clusters=2, random_state=0).fit(X)
    df = df.assign(cluster_label=af.labels_)
    hm = df.pivot(index="fov", columns="n", values="cluster_label")
    sns.heatmap(hm[::-1], cmap="crest")
    # plt.title("Cluster Classes (Remove all $\lambda_2=0$)")
    plt.title("Cluster Classification (k=2)")
    plt.xlabel("N")
    plt.ylabel("$\phi$")
    plt.show()

def radius_3d(df):
    # df = df.loc[df["conn_components"] <= 1]
    # creating figures
    print(len(df))
    df = df.loc[df['lambda_2_500'] == 1]
    # df = df.loc[df['n'] < 12]
    df = df.loc[df["omega"] == 20]
    df = df.loc[df["fov"] < 360 / df["n"]]
    print(len(df))

    x = df.loc[:, "n"]
    y = df.loc[:, "fov"]
    z = df.loc[:, "v"]
    colo = df.loc[:, "radius"]
    # print(min(colo), max(colo))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # setting color bar
    color_map = cm.ScalarMappable(cmap=cm.plasma)
    color_map.set_array(colo)

    # print(len(x), len(y), len(z))

    # creating the heatmap
    img = ax.scatter(x, y, z, marker='s',
                     s=200, c=colo, cmap='plasma')
    plt.colorbar(color_map)

    ax.set_title("Data Filtered by lambda_2 > 0")
    ax.set_xlabel('No. Agents')
    ax.set_ylabel('$\phi$')
    ax.set_zlabel('$\omega_{max}$')

    plt.show()

def cluster_3d(df):
    # df = df.loc[df["conn_components"] <= 1]
    # creating figures
    print(len(df))
    df = df.loc[df["fov"] < 360 / df["n"]]
    # df = df.loc[df['n'] < 12]
    df = df.loc[df["v"] == 1.0]
    print(len(df))

    x = df.loc[:, "n"]
    y = df.loc[:, "fov"]
    z = df.loc[:, "omega"]

    X = df.loc[:, "average_speed":"group_rotation"]
    print(X.shape)
    af = KMeans(n_clusters=4, random_state=0).fit(X)
    df = df.assign(cluster_label=af.labels_)
    colo = df.loc[:, "cluster_label"]

    # print(min(colo), max(colo))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # setting color bar
    color_map = cm.ScalarMappable(cmap=cm.plasma)
    color_map.set_array(colo)

    # print(len(x), len(y), len(z))

    # creating the heatmap
    img = ax.scatter(x, y, z, marker='s',
                     s=200, c=colo, cmap='plasma')
    # plt.colorbar(color_map)

    ax.set_title("Clustered Data (k=4)")
    ax.set_xlabel('No. Agents')
    ax.set_ylabel('$\phi$')
    ax.set_zlabel('$\omega_{max}$')

    plt.show()

def plot_circle_radius(df):
    v, omega = 1.0, 60.0
    slice_df = df.loc[df["v"] == v]
    slice_df = slice_df.loc[slice_df["omega"] == omega]

    X = np.arange(4, 31, 2)
    Y = np.arange(3, 76, 3)
    X, Y = np.meshgrid(X, Y)
    R = np.zeros_like(X) - 1

    for i in range(len(Y)):
        inner_slice = slice_df.loc[slice_df["fov"] == int(Y[i][0])]
        # print(int(Y[i][0]))
        # print(inner_slice)
        for j in range(len(Y[i])):
            row = inner_slice.loc[inner_slice["n"] == int(X[i][j])]
            # print(f"Query: {Y[i][j], int(X[i][j])}")
            # print(row)
            radius = row["radius"].item()
            manifold = row["fov"].item() > (360 / row["n"].item())
            if manifold:
                continue
            R[i][j] = radius

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # surf = ax.plot_surface(X, Y, R, cmap=cm.coolwarm,
    #                        linewidth=0, antialiased=False)
    #
    # ax.set_zlim(-1, np.max(R))
    # ax.zaxis.set_major_locator(LinearLocator(10))
    #
    # fig.colorbar(surf, shrink=0.5, aspect=5)

    width = depth = 2
    ax.bar3d(X.flatten(), Y.flatten(), np.zeros_like(R).flatten(), width, depth, R.flatten(), color='red')

    plt.show()

if __name__ == "__main__":
    df = pd.read_csv(RESULTS_FILE)

    plot_circle_radius(df)

    # Remove all
    # df =
    # X = df.loc[:, "average":""]
