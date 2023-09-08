import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.tree import export_text
import graphviz

from src.novel_swarms.config.AgentConfig import AgentYAMLFactory
from src.novel_swarms.config.WorldConfig import WorldYAMLFactory
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.NoveltyArchive import NoveltyArchive
from src.novel_swarms.results.results import main as report

# RESULTS_GENOTYPES = "../../../demo/evolution/noveltysearch/out/g_g100_p100.csv"
# RESULTS_PHENOTYPES = "../../../demo/evolution/noveltysearch/out/b_g100_p100.csv"

RESULTS_GENOTYPES = "../../../demo/evolution/noveltysearch/out/full_sweep_g.csv"
RESULTS_PHENOTYPES = "../../../demo/evolution/noveltysearch/out/full_sweep_b.csv"

def predict_connectivity():
    gdf = pd.read_csv(RESULTS_GENOTYPES)
    pdf = pd.read_csv(RESULTS_PHENOTYPES)

    gdf.columns = ["v0", "w0", "v1", "w1"]
    pdf.columns = ["AvgSpeed", "AngularMomentum", "RadialVariance", "Scatter", "GroupRotation", "Connectivity"]

    combined = pd.concat([gdf, pdf], axis=1)

    connected = combined.loc[combined["Connectivity"] == 1]
    not_connected = combined.loc[combined["Connectivity"] == 0]

    clf = DecisionTreeClassifier(random_state=0, max_depth=2)

    controllers = combined[["v0", "w0", "v1", "w1"]].to_numpy()
    print(controllers)
    connectivity = combined["Connectivity"].to_numpy()
    print(connectivity)

    clf.fit(controllers, connectivity)

    # r = tree.export_text(clf, feature_names=list(gdf.columns))
    # print(r)

    tree.plot_tree(clf, feature_names=list(gdf.columns), class_names=["Not Connected", "Connected"], filled=True)
    plt.show()


def predict_circle():
    gdf = pd.read_csv(RESULTS_GENOTYPES)
    pdf = pd.read_csv(RESULTS_PHENOTYPES)

    gdf.columns = ["v0", "w0", "v1", "w1"]
    pdf.columns = ["AvgSpeed", "AngularMomentum", "RadialVariance", "Scatter", "GroupRotation", "Connectivity"]

    rad0 = [gdf.loc[i]['v0'] / (abs(gdf.loc[i]["w0"]) if gdf.loc[i]["w0"] != 0 else 1000000) for i in range(len(gdf))]
    rad1 = [gdf.loc[i]['v1'] / (abs(gdf.loc[i]["w1"]) if gdf.loc[i]["w1"] != 0 else 1000000) for i in range(len(gdf))]

    gdf['rad0'] = rad0
    gdf['rad1'] = rad1

    combined = pd.concat([gdf, pdf], axis=1)
    clf = DecisionTreeClassifier(random_state=0, max_depth=3)

    controllers = combined[["v0", "w0", "v1", "w1", "rad0", "rad1"]].to_numpy()
    r_var = combined["RadialVariance"].to_numpy()
    r_var_binary = [1 if r_var[i] < 0.002 else 0 for i in range(len(r_var))]

    clf.fit(controllers, r_var_binary)

    # r = tree.export_text(clf, feature_names=list(gdf.columns))
    # print(r)

    # tree.plot_tree(clf, feature_names=list(gdf.columns), class_names=["Not Circle", "Circle"], filled=True)
    g_viz = tree.export_graphviz(clf, out_file=None, feature_names=list(gdf.columns), class_names=["Not Circle", "Circle"], filled=True)
    graph = graphviz.Source(g_viz)
    graph.render('decision_tree', view=True)

    # plt.show()

def cluster_by_connectivity():
    gdf = pd.read_csv(RESULTS_GENOTYPES)
    pdf = pd.read_csv(RESULTS_PHENOTYPES)

    gdf.columns = ["v0", "w0", "v1", "w1"]
    pdf.columns = ["AvgSpeed", "AngularMomentum", "RadialVariance", "Scatter", "GroupRotation", "Connectivity"]

    combined = pd.concat([gdf, pdf], axis=1)

    connected = combined.loc[combined["Connectivity"] == 1]

    not_connected = combined.loc[combined["Connectivity"] == 0]

    conn_controllers = connected[["v0", "w0", "v1", "w1"]].to_numpy()
    conn_behavior = connected[["AvgSpeed", "AngularMomentum", "RadialVariance", "Scatter", "GroupRotation"]].to_numpy()

    disconn_controllers = not_connected[["v0", "w0", "v1", "w1"]].to_numpy()
    disconn_behavior = not_connected[["AvgSpeed", "AngularMomentum", "RadialVariance", "Scatter", "GroupRotation"]].to_numpy()

    print(f"Disconnected Phenotypes: {len(disconn_controllers)}, Connected: {len(conn_controllers)}")

    connected_archieve = NoveltyArchive()
    connected_archieve.archive = conn_behavior
    connected_archieve.genotypes = conn_controllers

    disconnected_archive = NoveltyArchive()
    disconnected_archive.archive = disconn_behavior
    disconnected_archive.genotypes = disconn_controllers

    flockbot = AgentYAMLFactory.from_yaml("../../../demo/configs/flockbots-ns/flockbot.yaml")
    flockbot.seed = 0
    flockbot.rescale(10)

    world = WorldYAMLFactory.from_yaml("../../../demo/configs/flockbots-ns/world.yaml")
    world.seed = 0
    T, N = 3000, 13
    world.population_size = N
    # world.stop_at = T
    world.factor_zoom(zoom=10)
    world.addAgentConfig(flockbot)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world
    # results_config.archive = connected_archieve
    # report(config=results_config)

    results_config.archive = disconnected_archive
    report(config=results_config)


if __name__ == "__main__":
    predict_circle()
