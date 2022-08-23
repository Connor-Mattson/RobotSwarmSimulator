import time

import numpy as np
from sklearn.neighbors import NearestNeighbors


class NoveltyArchive:

    def __init__(self, max_size=None, from_file=None):
        self.archive = np.array([])
        self.max_size = max_size
        if from_file is not None:
            self.initializeFromFile(from_file)

    def addToArchive(self, vec):
        if len(self.archive) == 0:
            self.archive = np.array([vec])
            return

        self.archive = np.concatenate((self.archive, [vec]))
        if self.max_size and len(self.archive) > self.max_size:
            self.archive = self.archive[1:]

    def kNearestDistances(self, k, vec):
        """
        Given an integer, k, calculate the k nearest neighbors in the archive to the provided vector 'vec'
        Return an array of the distances to those neighbors from 'vec'

        Note: Uses unsupervised NN from sklearn.neighbors
        (see: https://scikit-learn.org/stable/modules/neighbors.html)
        """
        query = np.array([vec])
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(self.archive)
        distances, _ = nbrs.kneighbors(query)
        return distances[0]  # Returns a 1D np array

    def getNovelty(self, k, vec):
        # Compute with k = k + 1 because the value vec is in the archive space
        distances = self.kNearestDistances(k + 1, vec)
        novelty_score = sum(distances) / k
        return novelty_score

    def saveArchive(self, name=None):
        name = "out/" + name + "_" + str(int(time.time())) + ".csv"
        f = open(name, "w")

        for point in self.archive:
            line = ""
            for i, val in enumerate(point):
                line += str(val)
                if i < len(point) - 1:
                    line += ", "
            line += "\n"
            f.write(line)

        f.close()

    def initializeFromFile(self, filename):
        name = "out/" + filename
        f = open(name, "r")
        lines = f.readlines()
        for line in lines:
            line_list = line.split(",")
            float_list = []
            for i in line_list:
                float_list.append(float(i))
            float_list = np.array([float_list])
            if len(self.archive) == 0:
                self.archive = float_list
            else:
                self.archive = np.concatenate((self.archive, float_list))


