import math
import random
import numpy as np
from .NoveltyArchive import NoveltyArchive
from ..config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from ..results.Trends import Trends
from ..world.WorldFactory import WorldFactory
from ..util.timer import Timer
from ..util.processing.multicoreprocessing import MultiWorldSimulation


class OptimizedBehaviorDiscovery:
    """
    A Genetic Algorithm that will run many simulations of agent interaction and search for novel
    controllers.
    """

    def __init__(self, generations=10, population_size=20, crossover_rate=0.3, mutation_rate=0.1, genome_builder=None,
                 lifespan=200, world_config=None, behavior_config=None, k_neighbors=15, tournament_members=10,
                 mutation_flip_chance=0.2, allow_external_archive=False, genome_dependent_world=None, force_repeats=False,
                 seed=None, num_threads=1):
        self.population = np.array([])
        self.behavior = np.array([])
        self.scores = np.array([])
        self.lifespan = lifespan
        self.total_generations = generations
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.curr_genome = 0
        self.curr_generation = 0
        self.crossovers = 0
        self.mutations = 0
        self.mutation_flip_chance = mutation_flip_chance
        self.world_config = world_config
        self.behavior_config = behavior_config
        self.archive = NoveltyArchive()
        self.k = k_neighbors
        self.status = "Initializing"
        self.score_history = []
        self.average_history = []
        self.max_theta = []
        self.min_theta = []
        self.tournament_members = tournament_members
        self.allow_external_archive = allow_external_archive
        self.force_repeats = force_repeats
        self.genome_dependent_world = genome_dependent_world
        if self.genome_dependent_world is None:
            self.genome_dependent_world = {}

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        if genome_builder is None:
            raise Exception("BehaviorDiscovery must be initialized with a genotype ruleset.")
        self.gene_builder = genome_builder
        self.initializePopulation()

        # Initialize Multi-Threaded Environment
        self.pool = MultiWorldSimulation(pool_size=num_threads)

    def initializePopulation(self):
        self.population = np.array([
            self.gene_builder.fetch_random_genome() for j in range(self.population_size)
        ])
        self.scores = np.array([0.0 for i in range(self.population_size)])
        self.behavior = np.array([[-1.0 for j in range(len(self.behavior_config))] for i in range(self.population_size)])

    def runEntireGeneration(self, screen=None, output_config=None):
        configs = []
        for i in range(self.population_size):
            conf = self.world_config.deep_copy()
            conf.agentConfig.controller = self.population[i]
            conf.stop_at = self.lifespan
            conf.metadata["id"] = (self.curr_generation * self.population_size) + self.curr_genome
            configs.append(conf)

        # Batch Simulate the Entire Generation
        ret = self.pool.batch_evaluation(configs, output_config)

        # Post-Process: Scrape behavior vector and output tensors
        outputs, behaviors, controllers = [], [], []
        for i, (world, output) in enumerate(ret):
            self.behavior[i] = world.getBehaviorVector()
            behaviors.append(self.behavior[i])
            controllers.append(world.population[0].controller)
            outputs.append(output)
            self.archive.addToArchive(self.behavior[i], world.population[0].controller)  # Assumes Homogeneity
        return outputs, behaviors, controllers

    def runSinglePopulation(self, screen=None, i=0, save=True, genome=None, seed=None, output_config=None, heterogeneous=False):
        """
        Evaluates the Novelty of a Single Genome located at the ith index
        """
        # print(f"Ratio Rule: {self.gene_builder.rules[-1].domain}")
        if genome is None:
            genome = self.population[i]

        self.status = "Simulation"
        if seed is not None:
            self.world_config.seed = seed

        if not heterogeneous:
            self.world_config.agentConfig.controller = genome
            # self.world_config.agentConfig.controller = [0.0, 0.0, 0.0, 0.0]
        else:
            # Currently Assumes Two Species Only
            self.world_config.agentConfig.from_n_species_controller(genome)
            self.world_config.agentConfig = self.world_config.agentConfig.clone()
            self.world_config.agentConfig.attach_world_config(self.world_config)

        for key in self.genome_dependent_world:
            # print("Setting Key!", key, " with Value: ", genome[self.genome_dependent_world[key]])
            setattr(self.world_config, key, genome[self.genome_dependent_world[key]])

        # If the genome is new, simulate
        world = WorldFactory.create(self.world_config)
        output = world.evaluate(self.lifespan, output_capture=output_config)
        behavior = world.getBehaviorVector()

        if save:
            self.behavior[i] = behavior
            self.archive.addToArchive(behavior, genome)
            return output
        return output, behavior

    def evaluate(self):
        self.status = "Evaluate"

        for i, behavior_vector in enumerate(self.behavior):
            novelty = self.archive.getNovelty(k=self.k, vec=behavior_vector)
            self.scores[i] = novelty

        best = max(self.scores)
        self.score_history.append(best)
        self.average_history.append(sum(self.scores) / len(self.scores))

    def evolve(self):
        self.crossovers = 0
        self.mutations = 0
        self.status = "Evolution"
        selection = np.array([self.tournamentSelection(participants=10) for _ in self.population])
        self.population = np.array([])

        # Crossover in pairs
        for i in range(0, len(selection) - 1, 2):
            parent_A = selection[i]
            parent_B = selection[i + 1]

            searching = True
            child_A, child_B = None, None
            while searching:
                child_A, child_B = self.crossOver(parent_A, parent_B)

                force_mutation = False
                if np.array_equal(child_A, child_B):
                    force_mutation = True

                if force_mutation:
                    # print("Forcing Mutation!")
                    a_mutated = False
                    while not a_mutated:
                        child_A, a_mutated = self.mutation(child_A)
                    b_mutated = False
                    while not b_mutated:
                        child_B, b_mutated = self.mutation(child_B)
                else:
                    child_A, _ = self.mutation(child_A)
                    child_B, _ = self.mutation(child_B)

                # Obey the rules established by the GeneBuilder
                if self.gene_builder.is_valid(child_A) and self.gene_builder.is_valid(child_B):
                    searching = False
                    child_A = self.gene_builder.round_to(child_A)
                    child_B = self.gene_builder.round_to(child_B)

            self.addToPopulation(child_A)
            self.addToPopulation(child_B)

    def results(self):
        self.status = "Complete"
        Trends().graphBest(self.score_history)
        Trends().graphAverage(self.average_history)
        # Trends().graphArchive(self.archive)
        Trends().plotMetricHistograms(self.archive)
        # Trends().graphThetaDiff(self.max_theta, self.min_theta)

    def tournamentSelection(self, participants=4):
        player_indexes = np.random.randint(0, len(self.population), participants)
        scores = [(self.scores[i], i) for i in player_indexes]
        scores.sort()
        scores = scores[::-1]  # Reverse List (So we have descending scores)

        # Highest scores are most likely to succeed
        p = 0.9
        selection_probability = [p * math.pow(1 - p, i) for i in range(participants)]
        roll = random.random()
        for i, p in enumerate(selection_probability):
            if roll < sum(selection_probability[:i]):
                return self.population[scores[i][1]]

        return self.population[scores[-1][1]]

    def crossOver(self, p1, p2):
        c1 = p1.copy()
        c2 = p2.copy()
        if random.random() < self.crossover_rate:
            self.crossovers += 1
            crossover_point = random.randint(1, len(p1) - 2)
            c1 = np.append(p1[:crossover_point], p2[crossover_point:])
            c2 = np.append(p2[:crossover_point], p1[crossover_point:])
        return c1, c2

    def mutation(self, child):
        has_mutated = False
        for i in range(len(child)):
            if self.gene_builder.rules[i].allow_mutation:
                if random.random() < self.mutation_rate:
                    child[i] = self.gene_builder.rules[i].step_in_domain(child[i])
                    self.mutations += 1
                    has_mutated = True

        return child, has_mutated

    def addToPopulation(self, vector):
        if len(self.population) == 0:
            self.population = np.array([vector])
            return
        # print(vector)
        self.population = np.concatenate((self.population, [vector]))

    def getBestScore(self):
        return max(self.scores)

    def getAverageScore(self):
        if len(self.average_history) == 0:
            return 0
        return self.average_history[-1]

    def getBestGenome(self):
        return self.population[np.where(self.scores == self.getBestScore())[0][0]]

    def round_genome(self, genome):
        rounded = []
        for i in genome:
            rounded.append(round(i, 1) + 0.0)
        return np.array(rounded)