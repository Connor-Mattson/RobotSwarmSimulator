import numpy as np
from .AbstractInit import AbstractInitialization


class FixedInitialization(AbstractInitialization):
    """
    FixedInitialization: Agent's (x, y, theta) are all defined in a CSV file
    """
    def __init__(self, file_in, scale=None):
        super().__init__()
        self.file_in = file_in
        values = np.loadtxt(file_in, delimiter=",")[:, 1:]
        self.scaled = False
        self.scale = 1
        self.positions = values.tolist()

        if scale is not None:
            self.scale = scale
            self.rescale(scale)

    def rescale(self, zoom_factor):
        self.scale = zoom_factor
        if not self.scaled:
            for line in self.positions:
                line[0] *= zoom_factor
                line[1] *= zoom_factor
            self.scaled = True

    def as_dict(self):
        return {
            "type": "FixedInit",
            "file": self.file_in,
            "scale": self.scale
        }

    @staticmethod
    def from_dict(d):
        return FixedInitialization(d.get("file"), scale=d.get("scale", None))

    def getShallowCopy(self):
        return self.from_dict(self.as_dict())