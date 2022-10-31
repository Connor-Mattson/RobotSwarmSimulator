import math
import random
import numpy as np
from .NoveltyArchive import NoveltyArchive
from ..results.Trends import Trends
from ..world.WorldFactory import WorldFactory
from ..util.timer import Timer

def getRandomRoundedFloat(lower, _range):
    return round(((np.random.rand() * _range) + lower), 4)


class BehaviorDiscovery:
    """
    A Genetic Algorithm that will run many simulations of agent interaction and search for novel
    controllers.
    """

    def __init__(self, generations=10, population_size=20, crossover_rate=0.3, mutation_rate=0.1, genotype_rules=None,
                 lifespan=200, world_config=None, behavior_config=None, k_neighbors=15):
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
        self.world_config = world_config
        self.behavior_config = behavior_config
        self.archive = NoveltyArchive()
        self.k = k_neighbors
        self.status = "Initializing"
        self.score_history = []
        self.average_history = []
        self.max_theta = []
        self.min_theta = []

        if genotype_rules is None:
            raise Exception("BehaviorDiscovery must be initialized with a genotype ruleset.")
        self.geno_rules = genotype_rules

        self.initializePopulation()

    def initializePopulation(self):
        self.population = np.array([
            [rule.fetch() for rule in self.geno_rules] for j in range(self.population_size)
        ])
        self.scores = np.array([0.0 for i in range(self.population_size)])
        self.behavior = np.array([[-1.0 for j in range(len(self.behavior_config))] for i in range(self.population_size)])

    def runSinglePopulation(self, screen=None, i=0, save=True, genome=None, seed=None, output_config=None):
        """
        Evaluates the Novelty of a Single Genome located at the ith index
        """
        time_me = Timer("Single Population")
        if genome is None:
            genome = self.population[i]

        self.status = "Simulation"
        self.world_config.agentConfig.controller = genome

        time_world = Timer("World Factory")
        world = WorldFactory.create(self.world_config)
        time_world.check_watch()

        time_world = Timer("World Eval")
        output = world.evaluate(self.lifespan, output_capture=output_config)
        time_world.check_watch()
        if screen is not None:
            world.draw(screen)

        behavior = world.getBehaviorVector()
        time_me.check_watch()
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
        for i in range(0, len(selection), 2):
            parent_A = selection[i]
            parent_B = selection[i + 1]
            child_A, child_B = self.crossOver(parent_A, parent_B)
            child_A = self.mutation(child_A)
            child_B = self.mutation(child_B)
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
        for i in range(len(child)):
            if random.random() < self.mutation_rate:
                self.mutations += 1
                gene_rule = self.geno_rules[i]
                mutation_size = (gene_rule.mutation_step * 2 * np.random.rand()) - gene_rule.mutation_step
                child[i] = gene_rule.clip(child[i] + mutation_size)

        return child

    def addToPopulation(self, vector):
        if len(self.population) == 0:
            self.population = np.array([vector])
            return
        self.population = np.concatenate((self.population, [vector]))

    def getBestScore(self):
        return max(self.scores)

    def getAverageScore(self):
        if len(self.average_history) == 0:
            return 0
        return self.average_history[-1]

    def getBestGenome(self):
        return self.population[np.where(self.scores == self.getBestScore())[0][0]]
