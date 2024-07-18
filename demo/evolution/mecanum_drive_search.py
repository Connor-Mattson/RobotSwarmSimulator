import numpy as np

from src.novel_swarms.config.AgentConfig import MechanumAgentConfig
from src.novel_swarms.novelty.GeneRule import GeneRule, GeneRuleContinuous
from src.novel_swarms.novelty.evolve import main as evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.world.initialization.RandomInit import RectRandomInitialization

if __name__ == "__main__":
    BL = 10
    GUI_PADDING = 15
    N_AGENTS = 10
    WIDTH, HEIGHT = int(BL * 50), int(BL * 50)

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=52 / 2,
            distance=(BL * 5.7142),
            degrees=True,
            false_positive=0.0,
            false_negative=0.0,
            walls=None,
            show=True,
        )
    ])

    agent_config = MechanumAgentConfig(
        lx=(BL) / 2,
        ly=(BL * 0.9142) / 2,
        wheel_radius=BL * 0.57,
        dt=0.13,
        sensors=sensors,
        seed=None,
        idiosyncrasies=False
    )

    # Create a Genotype Ruleset that matches the size and boundaries of your robot controller _max and _min represent
    # the maximum and minimum acceptable values for that index in the genome. mutation_step specifies the largest
    # possible step in any direction that the genome can experience during mutation.
    genotype = [
        GeneRuleContinuous(_max=BL * 1.0, _min=BL * -1.0, mutation_step=BL * 0.1, round_digits=4),  #vx0
        GeneRuleContinuous(_max=BL * 1.0, _min=BL * -1.0, mutation_step=BL * 0.1, round_digits=4),  #vy0
        GeneRuleContinuous(_max=np.radians(130), _min=-np.radians(130), mutation_step=np.radians(50), round_digits=4),  #dtheta0
        GeneRuleContinuous(_max=BL * 1.0, _min=BL * -1.0, mutation_step=BL * 0.1, round_digits=4),  #vx1
        GeneRuleContinuous(_max=BL * 1.0, _min=BL * -1.0, mutation_step=BL * 0.1, round_digits=4),  #vx1
        GeneRuleContinuous(_max=np.radians(130), _min=-np.radians(130), mutation_step=np.radians(50), round_digits=4),  #dtheta1
    ]

    # Use the default Behavior Vector (from Brown et al.) to measure the collective swarm behaviors
    phenotype = ConfigurationDefaults.BEHAVIOR_VECTOR

    world_config = RectangularWorldConfig(
        size=(WIDTH + GUI_PADDING, HEIGHT + GUI_PADDING),
        n_agents=N_AGENTS,
        seed=None,
        behavior=phenotype,
        agentConfig=agent_config,
        padding=GUI_PADDING,
        collide_walls=False,
        show_walls=False,
        # init_type=None,
        init_type=RectRandomInitialization(num_agents=N_AGENTS, bb=((200, 200), (300, 300))),
    )

    GEN, POP = 15, 15
    novelty_config = GeneticEvolutionConfig(
        gene_rules=genotype,
        phenotype_config=phenotype,
        n_generations=GEN,
        n_population=POP,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=min(POP - 1, 15),
        simulation_lifespan=1200,
        display_novelty=False,
        save_archive=True,
        show_gui=True
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config)

    results_config = ConfigurationDefaults.RESULTS
    results_config.k = 8
    results_config.world = world_config
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config)
