from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.world.RectangularWorld import RectangularWorld


class WorldFactory:
    @staticmethod
    def create(config):
        if isinstance(config, RectangularWorldConfig):
            return RectangularWorld(config=config)
