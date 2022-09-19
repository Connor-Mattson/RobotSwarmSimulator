from ..config.WorldConfig import RectangularWorldConfig
from .RectangularWorld import RectangularWorld


class WorldFactory:
    @staticmethod
    def create(config):
        if isinstance(config, RectangularWorldConfig):
            return RectangularWorld(config=config)
