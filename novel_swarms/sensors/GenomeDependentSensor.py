from .BinaryLOSSensor import BinaryLOSSensor


class GenomeBinarySensor(BinaryLOSSensor):
    def __init__(self, genome_id: int, parent=None):
        super(GenomeBinarySensor, self).__init__(parent)
        self.genome_id = genome_id

    def augment_from_genome(self, genome):
        self.angle = genome[self.genome_id]
