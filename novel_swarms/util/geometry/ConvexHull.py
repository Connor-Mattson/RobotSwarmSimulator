from .Point import Point, PointAnglePair
from .Polygon import Polygon, Triangle
import numpy as np

class ConvexHull:
    def __init__(self, method="Graham"):
        self.method = method

    def find_hull(self, points):
        """
        Find the convex hull of a set of point objects, based on the `self.method` parameter.
        """
        if not (isinstance(points, list) or isinstance(points, set)):
            raise Exception("points parameter must be of type list or set")
        if not points:
            raise Exception("points parameter must be a list of size > 0")

        points = list(points)
        if not isinstance(points[0], Point):
            raise Exception("elements of points must be of type Point")

        if self.method == "Graham":
            return self._graham_scan(points)
        if self.method == "Wrapping":
            return self._gift_wrapping(points)


    def _graham_scan(self, points):
        poly = Polygon()
        if len(points) < 3:
            return poly

        # Sort Points by Angle Pair Relative to Left most Point
        base_point = self._find_min_x_value(points)
        assert base_point is not None

        point_angle_pairs = []
        for p in points:
            if p == base_point:
                continue
            angle = self._get_relative_angle(base_point, p, np.array([0, -1]))
            pair = PointAnglePair(p, angle)
            point_angle_pairs.append(pair)

        point_angle_pairs.sort()
        s = []
        s.append(base_point)
        for angle_pair in point_angle_pairs:
            s.append(angle_pair.p)
            if len(s) < 3:
                continue

            found = False
            while not found:
                r, q, p = s.pop(), s.pop(), s.pop()
                triangle = Triangle(p, q, r)
                if triangle.ccw():
                    found = True
                    s.append(p)
                    s.append(q)
                    s.append(r)
                else:
                    s.append(p)
                    s.append(r)

        poly.addPoint(base_point)
        for p in s:
            poly.addPoint(p)
        return poly

    def _gift_wrapping(self, points):
        poly = Polygon()
        if len(points) < 3:
            return poly

        max_Y = self._find_max_y_value(points)
        min_Y = self._find_min_y_value(points)
        i = 1000

        # Wrap Right Side
        consideration_p = min_Y
        while consideration_p != max_Y and i > 0:
            i -= 1
            poly.addPoint(consideration_p)
            min_angle = 10000
            min_point = None
            for p in points:
                if p == consideration_p:
                    continue
                angle = self._get_relative_angle(consideration_p, p, np.array([1, 0]))
                if angle < 0:
                    continue
                if angle < min_angle:
                    min_angle = angle
                    min_point = p
            consideration_p = min_point

        # Wrap Left Side
        consideration_p = max_Y
        while consideration_p != min_Y and i > 0:
            i -= 1
            poly.addPoint(consideration_p)
            min_angle = 10000
            min_point = None
            for p in points:
                if p == consideration_p:
                    continue
                angle = self._get_relative_angle(consideration_p, p, np.array([-1, 0]))
                if angle < 0:
                    continue
                if angle < min_angle:
                    min_angle = angle
                    min_point = p
            consideration_p = min_point

        if i < 1:
            return Polygon()
        return poly

    def _unit_vector(self, v):
        return v / np.linalg.norm(v)

    def _get_sidedness(self, e0, e1, p):
        v1 = np.array(e1.p - e0.p)
        v2 = np.array(p.p - e0.p)
        cross = np.cross(v1, v2)
        if cross < 0:
            return -1
        return 1

    def _get_relative_angle(self, base: Point, other : Point, basis_vec):
        base_to_other = np.array(other.p - base.p)
        base_endpoint = Point.from_vector(np.array(base.p + basis_vec))
        side = self._get_sidedness(base, base_endpoint, other)
        return np.arccos(np.clip(np.dot(self._unit_vector(basis_vec), self._unit_vector(base_to_other)), -1.0, 1.0)) * side

    def _find_min_x_value(self, points):
        min_X_Val = 100000
        min_X_Point = None
        for point in points:
            if point.x < min_X_Val:
                min_X_Val = point.x
                min_X_Point = point
        return min_X_Point

    def _find_min_y_value(self, points):
        min_Y_Val = 100000
        min_Y_Point = None
        for point in points:
            if point.y < min_Y_Val:
                min_Y_Val = point.y
                min_Y_Point = point
        return min_Y_Point

    def _find_max_y_value(self, points):
        max_Y_Val = -100000
        max_Y_Point = None
        for point in points:
            if point.y > max_Y_Val:
                max_Y_Val = point.y
                max_Y_Point = point
        return max_Y_Point