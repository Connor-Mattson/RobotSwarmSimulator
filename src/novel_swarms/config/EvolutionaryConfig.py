from ..novelty.GeneRule import GeneRule, GeneBuilder
from warnings import warn

class GeneticEvolutionConfig:
    def __init__(self,
                 gene_rules=None,
                 gene_builder=None,
                 phenotype_config=None,
                 n_generations=0,
                 n_population=0,
                 crossover_rate=0.0,
                 mutation_rate=0.0,
                 mutation_flip_chance=0.2,
                 world_config=None,
                 k_nn=15,
                 simulation_lifespan=0,
                 display_novelty=False,
                 save_archive=False,
                 show_gui=True,
                 save_every=None,
                 use_external_archive=False,
                 world_metadata = None
                 ):

        if gene_rules and not gene_builder:
            warn("The gene_rules parameter has been deprecated and will be removed in future versions. Use the gene_builder param instead in association with the GeneBuilder class", DeprecationWarning, stacklevel=2)
            self.gene_builder = GeneBuilder(rules=gene_rules)

        else:
            self.gene_builder = gene_builder

        self.generations = n_generations
        self.population = n_population
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.world_config = world_config
        self.behavior_config = phenotype_config
        self.k = k_nn
        self.lifespan = simulation_lifespan
        self.display_novelty = display_novelty
        self.save_archive = save_archive
        self.show_gui = show_gui
        self.save_every = save_every
        self.mutation_flip_chance = mutation_flip_chance
        self.use_external_archive = use_external_archive
        self.world_metadata = world_metadata

