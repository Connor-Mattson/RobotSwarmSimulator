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

    c = [-0.12, -0.2, 1.0, -1.0, 0.8, 0.9, 0.5, 0.6, 0.3]

    SEED = 3
    random.seed(SEED)

    sensors = SensorSet([
        BinaryLOSSensor(angle=0, draw=False),
    ])

    agent_config_A = DiffDriveAgentConfig(
        sensors=sensors,
        trace_length=180,
        agent_radius=12,
        wheel_radius=1,
        body_color=(0, 0, 0),
        trace_color=(0, 0, 0),
        body_filled=True,
    )

    agent_config_B = DiffDriveAgentConfig(
        sensors=sensors,
        trace_length=180,
        agent_radius=12,
        wheel_radius=1,
        body_color=(0, 0, 0),
        trace_color=(0, 0, 0),
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

