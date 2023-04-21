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

    def graphThetaDiff(self, max_theta_history, min_theta_history):
        fig, ax = plt.subplots()
        ax.set_title("Maximum and Minimum selections for Theta")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Angle (θ)")

        X = [i + 1 for i in range(len(max_theta_history))]
        ax.plot(X, max_theta_history, color='r', label='max θ')
        ax.plot(X, min_theta_history, color='b', label='min θ')
        plt.show()

    def graphArchiveComparisons(self, archive):
        point_size = 1

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Angular Momentum")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 1], marker='.', s=point_size)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Scatter")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 3], marker='.', s=point_size)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Radial Variance")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 2], marker='.', s=point_size)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Group Rotation vs Average Speed")
        ax.scatter(archive.archive[:, 4], archive.archive[:, 0], marker='.', s=point_size)
        plt.show()

    def plotMetricHistograms(self, archive):
        fig, ax = plt.subplots()
        ax.set_title("Group Rotation Distribution")
        ax.hist(archive.archive[:, 4], bins=20)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Algebraic Connectivity")
        ax.hist(archive.archive[:, 5], bins=20)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Angular Momentum Distribution")
        ax.hist(archive.archive[:, 1], bins=20)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Average Speed Distribution")
        ax.hist(archive.archive[:, 0], bins=20)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Radial Variance Distribution")
        ax.hist(archive.archive[:, 2], bins=20)
        plt.show()

        fig, ax = plt.subplots()
        ax.set_title("Scatter Distribution")
        ax.hist(archive.archive[:, 3], bins=20)
        plt.show()

