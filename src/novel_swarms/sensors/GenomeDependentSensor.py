import numpy as np

from .BinaryLOSSensor import BinaryLOSSensor
from .BinaryFOVSensor import BinaryFOVSensor


class GenomeBinarySensor(BinaryLOSSensor):
    def __init__(self, genome_id: int, parent=None, draw=True):
        super(GenomeBinarySensor, self).__init__(parent, draw=draw)
        self.genome_id = genome_id

    def augment_from_genome(self, genome):
        self.angle = genome[self.genome_id]


class GenomeFOVSensor(BinaryFOVSensor):
    def __init__(self, parent=None, fov_angle_id=None, fov_angle_default=14, distance_id=None, distance_default=10,
                 bias=None, degrees=True, false_positive=0.1, false_negative=0.05, walls=None, wall_sensing_range=None,
                 time_step_between_sensing=2, store_history=True):
        super(GenomeFOVSensor, self).__init__(parent, bias=bias, degrees=degrees, false_positive=false_positive,
                                              false_negative=false_negative, walls=walls, wall_sensing_range=wall_sensing_range,
                                              time_step_between_sensing=time_step_between_sensing,
                                              store_history=store_history)
        self.fov_angle_id = fov_angle_id
        self.fov_default = fov_angle_default
        self.distance_id = distance_id
        self.distance_default = distance_default
        self.degrees = degrees

    def augment_from_genome(self, genome):
        if self.fov_angle_id is not None:
            angle = genome[self.fov_angle_id]
            self.theta = np.radians(angle) if self.degrees else angle
        else:
            self.theta = self.fov_default

        if self.distance_id is not None:
            self.r = genome[self.distance_id]
        else:
            self.r = self.distance_default
