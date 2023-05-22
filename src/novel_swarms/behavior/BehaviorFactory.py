from ..behavior.AgentsAtGoal import AgentsAtGoal
from ..behavior.AverageSpeed import AverageSpeedBehavior
from ..behavior.AlgebraicConnectivity import AlgebraicConn
from ..behavior.ScatterBehavior import ScatterBehavior
from ..behavior.DistanceToGoal import DistanceToGoal
from ..behavior.TotalCollisions import TotalCollisionsBehavior
from ..behavior.AngularMomentum import AngularMomentumBehavior
from ..behavior.Centroid import Centroid
from ..behavior.ConvexHull import ConvexHull
from ..behavior.DistanceToGoal import DistanceToGoal
from ..behavior.GroupRotationBehavior import GroupRotationBehavior
from ..behavior.RadialVariance import RadialVarianceBehavior
from ..behavior.SensorOffset import GeneElementDifference
from ..behavior.SensorRotation import SensorRotation
from ..behavior.SensorSignal import SensorSignalBehavior

class BehaviorFactory:
    @staticmethod
    def create(d):
        if d["name"] == "Goal_Agents":
            return AgentsAtGoal(history=d["history_size"])
        elif d["name"] == "Alg_Connectivity":
            return AlgebraicConn(history=d["history_size"])
        elif d["name"] == "Angular_Momentum":
            return AngularMomentumBehavior(history=d["history_size"])
        elif d["name"] == "Average_Speed":
            return AverageSpeedBehavior(history=d["history_size"])
        elif d["name"] == "Centroid":
            return Centroid(history=d["history_size"])
        elif d["name"] == "Convex_Hull_Area":
            return ConvexHull(history=d["history_size"])
        elif d["name"] == "Goal_Dist":
            return DistanceToGoal(history=d["history_size"])
        elif d["name"] == "Group_Rotation":
            return GroupRotationBehavior(history=d["history_size"])
        elif d["name"] == "Radial_Variance":
            return RadialVarianceBehavior(history=d["history_size"])
        elif d["name"] == "Scatter":
            return ScatterBehavior(history=d["history_size"])
        # elif d["name"] == "Sensor_Offset":
        #     return GeneElementDifference(history=d["history_size"])
        # elif d["name"] == "Sensor_Rotation":
        #     return SensorRotation(history=d["history_size"])
        elif d["name"] == "Total_Collisions":
            return TotalCollisionsBehavior(history=d["history_size"])
        else:
            raise Exception(f"Cannot Construct Behavior of Type {d['name']}")
