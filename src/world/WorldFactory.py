from src.config.WorldConfig import RectangularWorldConfig
from src.world.RectangularWorld import RectangularWorld


class WorldFactory:
    @staticmethod
    def create(config):
        if isinstance(config, RectangularWorldConfig):
            return RectangularWorld(config=config)
