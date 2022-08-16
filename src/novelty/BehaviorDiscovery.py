import math
import random
import numpy as np
import pygame
from src.novelty.NoveltyArchive import NoveltyArchieve
from src.world.RectangularWorld import RectangularWorld

class BehaviorDiscovery():
    """
    A Genetic Algorithm that will run many simulations of agent interaction and search for novel
    controllers.
    """

    def __init__(self, generations=10, population_size=20, crossover_rate=0.3, mutation_rate=0.1,
         lifespan=1000, world_size = [100, 100], agents=30, k_neighbors = 15):
        self.population = np.array([])
        self.behavior = np.array([])
        self.scores = np.array([])
        self.lifespan = lifespan
        self.total_generations = generations
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.world_size = world_size
        self.curr_genome = 0
        self.curr_generation = 0
        self.crossovers = 0
        self.mutations = 0
        self.num_agents = agents
        self.archive = NoveltyArchieve(max_size = 10000)
        self.k = k_neighbors
        self.status = "Initializing"
        self.initializePopulation()

    def initializePopulation(self):
        LOWER_BOUND = -1
        UPPER_BOUND = 1
        RANGE = UPPER_BOUND - LOWER_BOUND
        GENE_SIZE = 4
        BEHAVIOR_SIZE = 5

        self.population = [
            [self.getRandomRoundedFloat(LOWER_BOUND, RANGE) for i in range(GENE_SIZE)] for j in range(self.population_size)
        ]
        self.scores = np.array([0.0 for i in range(self.population_size)])
        self.behavior = np.array([[-1 for j in range(BEHAVIOR_SIZE)] for i in range(self.population_size)])

    def runSingleGeneration(self, screen, i):
        """
        Evaluates the Novelty of a Single Genome located at the ith index
        """
        self.status = "Simulation"
        genome = self.population[i]
        world = RectangularWorld(self.world_size[0], self.world_size[1], pop_size=self.num_agents)
        world.setup(controller=genome)
        world.evaluate(self.lifespan)
        world.draw(screen)

        behavior = world.getBehaviorVector()
        self.behavior[i] = behavior
        self.archive.addToArchive(behavior)

    def evaluate(self, screen):
        self.status = "Evaluation"

        for i, behavior_vector in enumerate(self.behavior):
            novelty = self.archive.getNovelty(k=self.k, vec=behavior_vector)
            self.scores[i] = novelty
        
        best = max(self.scores)

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

        print(self.population)

    def tournamentSelection(self, participants = 4):
        player_indexes = np.random.randint(0, len(self.population), participants)
        scores = [(self.scores[i], i) for i in player_indexes]
        scores.sort()

        # Highest scores are most likely to succeed
        p = 0.8
        selection_probability = [p * math.pow(1-p, i) for i in range(participants)]
        roll = random.random()
        for i, p in enumerate(selection_probability):
            if(roll < sum(selection_probability[:i])):
                return self.population[scores[i][1]]
                
        return self.population[scores[-1][1]]

    def crossOver(self, p1, p2):
        c1 = p1.copy()
        c2 = p2.copy()
        if(random.random() < self.crossover_rate):
            self.crossovers += 1
            crossover_point = random.randint(1, len(p1) - 2)
            c1 = np.append(c1[:crossover_point], c2[crossover_point:])
            c2 = np.append(c2[:crossover_point], c1[crossover_point:])
        return c1, c2

    def mutation(self, child):
        for i in range(len(child)):
            if(random.random() < self.mutation_rate):
                self.mutations += 1
                child[i] += (random.random() * 0.6) - 0.3
        return child


    def addToPopulation(self, vector):
        if(len(self.population) == 0):
            self.population = np.array([vector])
            return
        self.population = np.concatenate((self.population, [vector]))

    def getRandomRoundedFloat(self, lower, _range):
        return round(((np.random.rand() * _range) + lower), 2)

    def getBestScore(self):
        return max(self.scores)

    def getBestGenome(self):
        return self.population[np.where(self.scores == self.getBestScore())[0][0]]
    
