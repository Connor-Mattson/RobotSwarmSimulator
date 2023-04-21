import numpy as np

from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
import random
import pandas

def cyclic_pursuit_detection():
    df_r_var = pandas.read_csv("out/r-var-cyclic.csv", header=0, index_col=0)
    df_sim_time = pandas.read_csv("out/sim-time-cyclic.csv", header=0, index_col=0)

    r_var = -df_r_var.to_numpy()
    sim_time = df_sim_time.to_numpy()
    print(r_var)
    # r_var = np.clip(r_var, 0.00099, 0.001)
    # # r_var = np.exp(-r_var)
    # print(r_var)
    combined_r = np.flip(r_var + sim_time, axis=0)
    r_var_flipped = np.flip(np.round(np.clip(r_var, 0, 0.02), 3), axis=0)

    df_r_var = pandas.DataFrame(r_var_flipped)
    print(df_r_var.values)

    x_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 1)]
    y_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 1)]
    y_tick_labels.reverse()

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(df_r_var, annot=False, ax=ax, square=True, cmap=sns.color_palette("rocket_r", as_cmap=True),
                cbar_kws={'shrink': 0.6})
    ax.set_xticklabels(x_tick_labels)
    ax.set_yticklabels(y_tick_labels)
    ax.set_xlabel("$V_{r0}$")
    ax.set_ylabel("$V_{l0}$")
    plt.title("Radial Variance (Cross section of $[V_{l1}, V_{r1}] = [1.0, 1.0])$")
    plt.tight_layout()
    plt.show()


def aggregation_detection():
    df_sim_time = pandas.read_csv("out/sim-time-aggregation.csv", header=0, index_col=0)

    combined_r = np.flip(df_sim_time.values, axis=0)
    df_sim_time = pandas.DataFrame(combined_r)

    x_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 2)]
    y_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 2)]
    y_tick_labels.reverse()

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(df_sim_time, annot=False, ax=ax, square=True, cmap=sns.color_palette("rocket_r", as_cmap=True),
                cbar_kws={'shrink': 0.6})
    ax.set_xticklabels(x_tick_labels)
    ax.set_yticklabels(y_tick_labels)
    ax.set_xlabel("$V_{r0}$")
    ax.set_ylabel("$V_{l0}$")
    plt.title("Aggregation Score (Cross section of $[V_{l1}, V_{r1}] = [1.0, -1.0])$")
    plt.tight_layout()
    plt.show()

def aggregation_detection_2():
    df_sim_time = pandas.read_csv("out/sim-time-aggregation-2.csv", header=0, index_col=0)

    combined_r = np.flip(df_sim_time.values, axis=0)
    df_sim_time = pandas.DataFrame(combined_r)

    x_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 1)]
    y_tick_labels = [str(round(i * 0.1, 1)) for i in range(-10, 11, 1)]
    y_tick_labels.reverse()

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(df_sim_time, annot=False, ax=ax, square=True, cmap=sns.color_palette("rocket_r", as_cmap=True),
                cbar_kws={'shrink': 0.6})
    ax.set_xticklabels(x_tick_labels)
    ax.set_yticklabels(y_tick_labels)
    ax.set_xlabel("$V_{r0}$")
    ax.set_ylabel("$V_{l0}$")
    plt.title("Aggregation Score (Cross section of $[V_{l1}, V_{r1}] = [1.0, -1.0])$")
    plt.tight_layout()
    plt.show()

def cyclic_3d_gradient_visualization():
    df_r_var = pandas.read_csv("out/r-var-cyclic.csv", header=0, index_col=0)
    df_sim_time = pandas.read_csv("out/sim-time-cyclic.csv", header=0, index_col=0)

    r_var = -df_r_var.to_numpy()
    sim_time = df_sim_time.to_numpy()
    print(r_var)
    # r_var = np.clip(r_var, 0.00099, 0.001)
    # # r_var = np.exp(-r_var)
    # print(r_var)
    combined_r = np.flip(r_var + sim_time, axis=0)
    r_var_flipped = np.flip(np.round(np.clip(r_var, 0, 0.02), 3), axis=0)

    df_r_var = pandas.DataFrame(r_var_flipped)
    print(df_r_var.values)


    x_plot = np.linspace(-1.0, 1.0, 21)
    y_plot = np.linspace(-1.0, 1.0, 21)
    plot_1, plot_2 = np.meshgrid(x_plot, y_plot)

    axes = plt.axes(projection="3d")
    axes.plot_surface(plot_1, plot_2, combined_r / -100)
    plt.title("Cyclic Pursuit Score (Cross section: $[V_{l1}, V_{r1}] = [1.0, 1.0])$")
    plt.xlabel("$V_{l0}$")
    plt.ylabel("$V_{r0}$")
    axes.set_zlabel("Score")
    plt.show()

def aggregation_3d_gradient_visualization():
    df_sim_time = pandas.read_csv("out/sim-time-aggregation-s1.csv", header=0, index_col=0)

    combined_r = np.flip(df_sim_time.values, axis=0)
    df_sim_time = pandas.DataFrame(combined_r)

    x_plot = np.linspace(-1.0, 1.0, 21)
    y_plot = np.linspace(-1.0, 1.0, 21)
    plot_1, plot_2 = np.meshgrid(x_plot, y_plot)

    axes = plt.axes(projection="3d")
    axes.plot_surface(plot_1, plot_2, combined_r / -100)
    plt.title("Aggregation Score (Cross section: $[V_{l1}, V_{r1}] = [1.0, 1.0])$")
    plt.xlabel("$V_{l0}$")
    plt.ylabel("$V_{r0}$")
    axes.set_zlabel("Score")
    plt.show()



if __name__ == "__main__":
    aggregation_3d_gradient_visualization()