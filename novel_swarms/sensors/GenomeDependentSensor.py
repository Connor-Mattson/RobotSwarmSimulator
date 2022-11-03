from .BinaryLOSSensor import BinaryLOSSensor


class GenomeBinarySensor(BinaryLOSSensor):
    def __init__(self, genome_id: int, parent=None, draw=True):
        super(GenomeBinarySensor, self).__init__(parent, draw=draw)
        self.genome_id = genome_id

    def augment_from_genome(self, genome):
        self.angle = genome[self.genome_id]
