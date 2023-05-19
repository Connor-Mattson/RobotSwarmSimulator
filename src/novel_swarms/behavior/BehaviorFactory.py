from src.novel_swarms.behavior.AgentsAtGoal import AgentsAtGoal
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.AlgebraicConnectivity import AlgebraicConn
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.Centroid import Centroid
from src.novel_swarms.behavior.ConvexHull import ConvexHull
from src.novel_swarms.behavior.DistanceToGoal import DistanceToGoal
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.SensorOffset import GeneElementDifference
from src.novel_swarms.behavior.SensorRotation import SensorRotation
from src.novel_swarms.behavior.SensorSignal import SensorSignalBehavior

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
