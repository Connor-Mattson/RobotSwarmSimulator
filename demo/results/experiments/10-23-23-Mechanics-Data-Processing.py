"""
Find the best Homogeneous Agents
"""
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

RESULTS_FILE = "../../../demo/results/out/SM-1698164058/sweep/genes.csv"

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
    # df = df.loc[df["lambda_2"] > 0]
    hm = df.pivot(index="fov", columns="n", values="radius")
    sns.heatmap(hm[::-1], cmap="crest")
    plt.title("Mill Radius (cm)")
    plt.xlabel("N")
    plt.ylabel("$\phi$")
    plt.show()

def cluster_and_report(df):

    # df = df.loc[(df["n"] < 14) | (df["fov"] <= 27)]
    df = df.loc[df["lambda_2_500"] == 1.0]
    X = df.loc[:, "average_speed":"group_rotation"]
    print(X.shape)
    af = KMeans(n_clusters=5, random_state=0).fit(X)
    df = df.assign(cluster_label=af.labels_)
    hm = df.pivot(index="fov", columns="n", values="cluster_label")
    sns.heatmap(hm[::-1], cmap="crest")
    plt.title("Cluster Classes (Remove all $\lambda_2=0$)")
    plt.xlabel("N")
    plt.ylabel("$\phi$")
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv(RESULTS_FILE)
    cluster_and_report(df)

    # Remove all
    # df =
    # X = df.loc[:, "average":""]
