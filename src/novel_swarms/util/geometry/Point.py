import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.p = np.array([self.x, self.y])

    def __repr__(self):
        return repr((self.x, self.y))

    def __eq__(self, other):
        if self.p is not None and other.p is not None:
            return np.array_equal(self.p, other.p)
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def dist(self, other):
        return np.linalg.norm(other.p - self.p)

    def __lt__(self, other):
        return self.x < other.x

    @staticmethod
    def from_agent(agent):
        return Point(agent.get_x_pos(), agent.get_y_pos())

    @staticmethod
    def from_vector(vector):
        return Point(vector[0], vector[1])

    @staticmethod
    def get_centroid(points):
        sum = np.array([0.0, 0.0])
        for p in points:
            sum += p.p
        sum /= len(points)
        return Point.from_vector(sum)

class PointAnglePair:
    def __init__(self, point, angle):
        self.p = point
        self.angle = angle

    def __repr__(self):
        return repr((self.p, self.angle))

    def __lt__(self, other):
        return self.angle < other.angle

    def __eq__(self, other):
        return self.angle == other.angle and self.p == other.p