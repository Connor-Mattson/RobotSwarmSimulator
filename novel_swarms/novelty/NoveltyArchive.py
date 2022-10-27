import time
import numpy as np
from sklearn.neighbors import NearestNeighbors


class NoveltyArchive:

    def __init__(self, max_size=None, pheno_file=None, geno_file=None, absolute=False):
        self.genotypes = np.array([])
        self.archive = np.array([])
        self.max_size = max_size
        self.time_stamp = None
        if pheno_file is not None and geno_file is not None:
            self.initializeFromFile(pheno_file, geno_file, absolute=absolute)

    def addToArchive(self, vec, genome=[]):
        if len(self.archive) == 0:
            self.archive = np.array([vec])
            self.genotypes = np.array([genome])
            return

        self.archive = np.concatenate((self.archive, [vec]))
        self.genotypes = np.concatenate((self.genotypes, [genome]))
        if self.max_size and len(self.archive) > self.max_size:
            self.archive = self.archive[1:]
            self.genotypes = self.genotypes[1:]

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

    def getTimeStamp(self):
        if self.time_stamp is None:
            self.time_stamp = int(time.time())
        return self.time_stamp

    def saveArchive(self, name=None):
        name = "out/" + name + "_" + str(self.getTimeStamp()) + ".csv"
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

    def saveGenotypes(self, name=None):
        name = "out/" + name + "_" + str(self.getTimeStamp()) + ".csv"
        f = open(name, "w")

        for point in self.genotypes:
            line = ""
            for i, val in enumerate(point):
                line += str(val)
                if i < len(point) - 1:
                    line += ", "
            line += "\n"
            f.write(line)

        f.close()

    def initializeFromFile(self, phenotype_file, genotype_file, absolute=False):
        name = "out/" + phenotype_file
        if absolute:
            name = phenotype_file
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

        name = "out/" + genotype_file
        if absolute:
            name = genotype_file
        f = open(name, "r")
        lines = f.readlines()
        for line in lines:
            line_list = line.split(",")
            float_list = []
            for i in line_list:
                float_list.append(float(i))
            float_list = np.array([float_list])
            if len(self.genotypes) == 0:
                self.genotypes = float_list
            else:
                self.genotypes = np.concatenate((self.genotypes, float_list))
