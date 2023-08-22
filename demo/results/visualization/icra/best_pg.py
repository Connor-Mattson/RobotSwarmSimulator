import random
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas
import numpy as np
import os


BASE_DATA_PATH = "../../out/Levy-Fixed-1"
PATH_SUFFIX = "CMAES/genomes.csv"
if __name__ == "__main__":

    results = np.zeros((5, 4))
    for i, t in enumerate([5000, 4000, 3000, 2000, 1000]):
        for j, n in enumerate([1, 10, 20, 30]):
            name = f"n{n}-t{t}-fixed"
            try:
                data = pandas.read_csv(os.path.join(BASE_DATA_PATH, name, PATH_SUFFIX))

                maximum_pg = max(data["Goal_Agents"])
                results[i, j] = maximum_pg
            except Exception as e:
                print(f"No file with name: {name}")
                results[i, j] = -10

    print(results)
