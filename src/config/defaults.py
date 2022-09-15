from src.behavior.AngularMomentum import AngularMomentumBehavior
from src.behavior.AverageSpeed import AverageSpeedBehavior
from src.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.behavior.RadialVariance import RadialVarianceBehavior
from src.behavior.ScatterBehavior import ScatterBehavior
from src.config.AgentConfig import DiffDriveAgentConfig
from src.config.ResultsConfig import ResultsConfig
from src.config.WorldConfig import RectangularWorldConfig
from src.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.sensors.SensorSet import SensorSet


class ConfigurationDefaults:

    SIMPLE_SENSOR = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    DIFF_DRIVE_AGENT = DiffDriveAgentConfig(
        sensors=SIMPLE_SENSOR,
    )

    BEHAVIOR_VECTOR = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    RECTANGULAR_WORLD = RectangularWorldConfig(
        size=(500, 500),
        n_agents=30,
        behavior=BEHAVIOR_VECTOR,
        padding=15
    )

    RESULTS = ResultsConfig(
        k_clusters=10,
        display_trends=False
    )

