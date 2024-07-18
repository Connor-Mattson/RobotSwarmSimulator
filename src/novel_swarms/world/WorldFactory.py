from ..config.WorldConfig import RectangularWorldConfig, PhysicsRectangularWorldConfig
from .RectangularWorld import RectangularWorld
from .PhysicsRectangularWorld import PhysicsRectangularWorld


class WorldFactory:
    @staticmethod
    def create(config):
        if isinstance(config, PhysicsRectangularWorldConfig):
            print("Its a physics world")
            return PhysicsRectangularWorld(config=config)
        elif isinstance(config, RectangularWorldConfig):
            return RectangularWorld(config=config)

