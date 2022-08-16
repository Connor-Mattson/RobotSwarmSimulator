import numpy as np
from sklearn.neighbors import NearestNeighbors

class NoveltyArchieve():
    archive = np.array([])
    
    def __init__(self, max_size=10000):
        self.max_size = max_size

    def addToArchive(self, vec):
        if len(self.archive) == 0:
            self.archive = np.array([vec])
            return

        self.archive = np.concatenate((self.archive, [vec]))
        if(len(self.archive) > self.max_size):
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
        return distances[0] # Returns a 1D np array

    def getNovelty(self, k, vec):
        distances = self.kNearestDistances(k, vec)
        return sum(distances) / len(distances)

        

