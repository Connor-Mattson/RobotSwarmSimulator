import matplotlib.pyplot as plt
import numpy as np

class Trends():
    def __init__(self):
        pass
    
    def graphBest(self, best_scores):
        fig, ax = plt.subplots()
        ax.set_title("Best Novelty Over Time")
        ax.plot(best_scores)
        plt.show()

    def graphAverage(self, average_scores):
        fig, ax = plt.subplots()
        ax.set_title("Average Novelty Over Time")
        ax.plot(average_scores)
        plt.show()

    def graphArchive(self, archive):
        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Angular Momentum")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 1], marker='.')
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Scatter")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 3], marker='.')
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Radial Variance")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 2], marker='.')
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Average Speed")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 0], marker='.')
        plt.show()