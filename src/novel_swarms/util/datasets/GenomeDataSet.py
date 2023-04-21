import numpy as np
from numpy import genfromtxt


def getArrayAsCSVLine(array_like):
    outstr = ""
    for i in range(len(array_like) - 1):
        outstr += str(round(array_like[i], 5)) + ", "
    outstr += str(round(array_like[-1], 5))
    outstr += "\n"
    return outstr


class GenomeDataSet:

    def __init__(self, file=None, array_like=None, name=None):
        self.data = []
        self.name = name
        if not file and not array_like:
            raise Exception("GenomeDataSet must be initialized with either the 'file' or 'array_like' parameter filled")
        if file is not None:
            self._loadFromFile(file)
            self.file = file
        else:
            self._loadFromArray(array_like)
            self.file = None

    def __len__(self):
        return len(self.data)

    def _loadFromFile(self, file_name):
        self.data = genfromtxt(file_name, delimiter=",")
        if self.data.shape == (0,):
            self.data = np.array([[0.0, 0.0, 0.0, 0.0]])
        if self.data.ndim == 1:
            self.data = np.expand_dims(self.data, axis=0)

    def _loadFromArray(self, array_like):
        self.data = array_like

    def append(self, elem):
        np.concatenate((self.data, [elem]))
        if self.file:
            f = open(self.file, "a")
            f.write(getArrayAsCSVLine(elem))
            f.close()

    def overwrite_data(self, array_like):
        self.data = array_like

    def save(self):
        if self.file:
            np.savetxt(self.file, X=np.array(self.data), delimiter=",")

