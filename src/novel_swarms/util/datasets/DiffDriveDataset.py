from src.novel_swarms.util import GenomeDataSet


class DiffDriveDataset(GenomeDataSet):

    _PRESET_BEHAVIOR_FILES = {
        "cyclic": "../../data/diffdrivegenomes/cyclic.csv",
        "aggregation": "../../data/diffdrivegenomes/aggregation.csv",
        "wall-following": "../../data/diffdrivegenomes/wall-following.csv",
        "dispersal": "../../data/diffdrivegenomes/dispersal.csv",
        "milling": "../../data/diffdrivegenomes/milling.csv",
        "random": "../../data/diffdrivegenomes/random.csv",
    }

    CYCLIC_PURSUIT = GenomeDataSet(_PRESET_BEHAVIOR_FILES["cyclic"], name="cyclic_pursuit")
    AGGREGATION = GenomeDataSet(_PRESET_BEHAVIOR_FILES["aggregation"], name="aggregation")
    WALL_FOLLOWING = GenomeDataSet(_PRESET_BEHAVIOR_FILES["wall-following"], name="wall_following")
    DISPERSAL = GenomeDataSet(_PRESET_BEHAVIOR_FILES["dispersal"], name="dispersal")
    MILLING = GenomeDataSet(_PRESET_BEHAVIOR_FILES["milling"], name="milling")
    RANDOM = GenomeDataSet(_PRESET_BEHAVIOR_FILES["random"], name="random")

    def __init__(self, file=None, array_like=None):
        super(DiffDriveDataset, self).__init__(file=file, array_like=array_like)
