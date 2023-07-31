import pygame
import time
import numpy as np
import random
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.novelty.GeneRule import GeneRule, GeneBuilder, GeneRuleContinuous
from src.novel_swarms.config.OutputTensorConfig import OutputTensorConfig
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.GenomeDependentSensor import GenomeBinarySensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.novelty.BehaviorDiscovery import BehaviorDiscovery
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # c = [0.7, 1.0, 0.4, 0.5, -0.9, -0.4, -0.3, 0.6, 12/24]  # Flower s16
    # c = [0.9, 1.0, 0.7, 0.7, 0.9, -0.7, 1.0, 0.8, 8/24]  # Eye s7
    # c = [0.0, 0.5, 0.6, -0.1, 0.3, 0.7, 0.6, 0.0, 8/24] # N-Cycles s15
    # c = [0.1, 0.5, 0.6, -0.1, 0.3, 0.7, 0.4, -0.4, 8/24]  # Spiral s5
    # c = [0.5, -0.7, 0.9, -0.5, 0.7, 1.0, 1.0, 0.5, 8/24]  # Nucleus s9
    # c = [-0.6, 1.0, 1.0, 0.4, 0.7, -0.6, 0.7, 1.0, 3/24]  # Flail s12
    # c = [-0.9, -0.8, -0.8, -1., -0.6, -1., 0.9, -0.7, 6/24]  # Perimeter s15
    # c = [0.2, 0.7, -0.3, -0.1, 0.1, 0.9, 1.0, 0.8, 4/24]  # Containment s12
    # c = [-0.7, 0.7, -0.4, -0.8, 0.8, 0.1, 0.2, 0.5, 1/24]  # Snake s76
    # c = [-0.1, -0.2, 1.0, -1.0, 0.8, 0.9, 0.9, 1.0, 6/24]  # Hurricane s76
    # c = [1.0, -1.0, 0.7, 0.5, 0.9, 0.7, -1.0, -0.2, 12/24]  # Dipole s76
    # c = [0.6, 1.0, 0.4, 0.5, 0.2, 0.7, -0.5, -0.1, 12/24]  # C+D s32
    # c = [0.1, 1.0, 0.3, 0.7, 0.2, 0.7, -0.5, -0.1, 12 / 24]  # A+D s32
    # c = [0.7, 1.0, 0.3, 0.4, 0.2, 0.7, -0.5, -0.1, 12 / 24]  # M+D s32
    c = [-0.4, -1.0, -0.2, 0.9, -0.6, 0.7, 0.9, 1.0, 3 / 24]  # Geometric Warp s15
    # c = [-0.3, 0.1,  -0.4, -0.3, -0.3, 0., -0.2, -0.1, 8/24]  # Dispersal s12
    # c = [-0.9, 0.6, 0.9, 0.7, -0.4, 0.1, 0.6, 0.2, 12/24]  # Segments s16
    # c = [0.4, -0.7, 0.9, -0.5, 0.9, -0.4, 1.0, 0.4, 8/24] # Aggregation s2
    # c = [1.0, 0.9, 0.9, 0.5, 0.7, 0.5, 1.0, 1.0, 12/24]  # Mill-Followers s17
    # c = [-0.9, 1.0, 1.0, 1.0, 0.1, -0.1, 0.0, 0.0, 12/24]  # Site Traversal s115
    # c = [0.7, 1.0, 0.4, 0.5, 0.7, 0.9, 0.4, 0.5, 8/24]  # Milling s1
    # c = [1.0, -0.1, -0.9, -1.0, 1.0, 0.6, -0.3, 0.9, 1/24]  # Wall-Following s2
    # c = [-0.7, 0.3, 1.0, 1.0, -0.7, 0.3, 1.0, 1.0, 12/24] # Cyclic Pursuit s2

    SEED = 5
    AGENT_RADIUS = 6
    random.seed(SEED)

    sensors = SensorSet([
        BinaryLOSSensor(angle=0, draw=False),
    ])

    agent_config_A = DiffDriveAgentConfig(
        sensors=sensors,
        trace_length=0,
        agent_radius=AGENT_RADIUS,
        wheel_radius=1,
        body_color=(255, 0, 0),
        trace_color=(255, 0, 0),
        body_filled=True,
    )

    agent_config_B = DiffDriveAgentConfig(
        sensors=sensors,
        trace_length=0,
        agent_radius=AGENT_RADIUS,
        wheel_radius=1,
        body_color=(0, 200, 0),
        trace_color=(0, 200, 0),
        body_filled=True,
    )

    heterogeneous_swarm = HeterogeneousSwarmConfig()
    heterogeneous_swarm.add_sub_populuation(agent_config_A, 12)
    heterogeneous_swarm.add_sub_populuation(agent_config_B, 12)
    heterogeneous_swarm.from_n_species_controller(c)

    gene_specifications = GeneBuilder(
        heuristic_validation=True,
        round_to_digits=1,
        rules=[
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            GeneRuleContinuous(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
            # GeneRule(_max=1.0, _min=-1.0, mutation_step=0.4, round_digits=1),
        ]
    )

    phenotype = []

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=18,
        seed=SEED,
        behavior=phenotype,
        agentConfig=heterogeneous_swarm,
        padding=15,
        background_color=(255, 255, 255)
    )

    pygame.init()
    pygame.display.set_caption("Evolutionary Novelty Search")
    screen = pygame.display.set_mode((world_config.w, world_config.h))

    output_config = OutputTensorConfig(
        timeless=True,
        total_frames=1,
        steps_between_frames=2,
        screen=screen,
        colored=True,
        background_color=(255,255,255)
    )

    # Original Experiment was 50 gens, 50 pop
    novelty_config = GeneticEvolutionConfig(
        gene_builder=gene_specifications,
        phenotype_config=phenotype,
        n_generations=50,
        n_population=50,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=15,
        simulation_lifespan=5000,
        display_novelty=False,
        save_archive=True,
        show_gui=False,
        mutation_flip_chance=0.2,
        use_external_archive=False,
        # save_every=1
    )

    # initialize the pygame module
    sim(world_config, show_gui=True)

