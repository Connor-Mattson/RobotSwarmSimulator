from ..novelty.GeneRule import GeneRule


class GeneticEvolutionConfig:
    def __init__(self,
                 gene_rules=None,
                 phenotype_config=None,
                 n_generations=0,
                 n_population=0,
                 crossover_rate=0.0,
                 mutation_rate=0.0,
                 world_config=None,
                 k_nn=15,
                 simulation_lifespan=0,
                 display_novelty=False,
                 save_archive=False,
                 show_gui=True,
                 save_every=None
                 ):

        if gene_rules is None or not isinstance(gene_rules, list) or len(gene_rules) == 0:
            raise Exception("Gene Rules with length > 0 must be provided to an instantiation of GeneticEvolutionConfig")
        if not isinstance(gene_rules[0], GeneRule):
            raise Exception("Elements of GeneRules parameter must be instances of GeneRule")

        self.gene_rules = gene_rules
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
