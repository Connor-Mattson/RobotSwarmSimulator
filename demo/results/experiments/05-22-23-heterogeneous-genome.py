from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.GeneRule import GeneBuilder, GeneRule
from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.novelty.evolve import main as evolve
from src.novel_swarms.results.results import main as report

SINGLE_SENSOR_HETEROGENEOUS_MODEL = GeneBuilder(
    round_to_digits=1,
    rules=[
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[i / 10 for i in range(-10, 11, 1)], step_size=4, allow_mutation=True),
        GeneRule(discrete_domain=[0.2, 0.25, 0.33, 0.5], step_size=2, allow_mutation=True)
    ]
)

def simulate_from_single_controller():
    c = [-1.0, 1.0, 0.3, 0.2, 0.3, -0.9, 0.4, 1.0, 0.3]
    n = 24

    agent_A = DiffDriveAgentConfig(controller=None, sensors=ConfigurationDefaults.SIMPLE_SENSOR, dt=1.0, body_color=(255, 0, 0), body_filled=True)
    agent_B = DiffDriveAgentConfig(controller=None, sensors=ConfigurationDefaults.SIMPLE_SENSOR, dt=1.0, body_color=(0, 255, 0), body_filled=True)

    h_config = HeterogeneousSwarmConfig()
    h_config.add_sub_populuation(agent_A, n // 2)
    h_config.add_sub_populuation(agent_B, n // 2)
    h_config.from_n_species_controller(c)

    world = ConfigurationDefaults.RECTANGULAR_WORLD
    world.agentConfig = h_config
    world.behavior = ConfigurationDefaults.BEHAVIOR_VECTOR
    world.collide_walls = True
    world.show_walls = True
    h_config.attach_world_config(world)

    w = sim(world, show_gui=True)
    return w


def evolve_heterogeneity():
    # Use the default Differential Drive Agent, initialized with a single sensor and normal physics
    agent_A = DiffDriveAgentConfig(controller=None, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.13, body_color=(255, 0, 0))
    agent_B = DiffDriveAgentConfig(controller=None, sensors=ConfigurationDefaults.FLOCKBOT_SENSOR_SET, dt=0.13, body_color=(0, 255, 0))
    h_config = HeterogeneousSwarmConfig()
    h_config.add_sub_populuation(agent_A, 24//2)
    h_config.add_sub_populuation(agent_B, 24//2)

    print(h_config.get_configs())

    # Create a Genotype Ruleset that matches the size and boundaries of your robot controller _max and _min represent
    # the maximum and minimum acceptable values for that index in the genome. mutation_step specifies the largest
    # possible step in any direction that the genome can experience during mutation.
    genotype = SINGLE_SENSOR_HETEROGENEOUS_MODEL

    # Use the default Behavior Vector (from Brown et al.) to measure the collective swarm behaviors
    phenotype = ConfigurationDefaults.BEHAVIOR_VECTOR

    # Define an empty Rectangular World with size (w, h) and n agents.
    world_config = ConfigurationDefaults.RECTANGULAR_WORLD
    world_config.behavior = phenotype
    world_config.agentConfig = h_config

    # Define the breath and depth of novelty search with n_generations and n_populations
    # Modify k_nn to change the number of nearest neighbors used in calculating novelty.
    # Increase simulation_lifespan to allow agents to interact with each other for longer.
    # Set save_archive to True to save the resulting archive to /out.
    novelty_config = GeneticEvolutionConfig(
        gene_builder=genotype,
        phenotype_config=phenotype,
        n_generations=20,
        n_population=20,
        crossover_rate=0.7,
        mutation_rate=0.15,
        world_config=world_config,
        k_nn=15,
        simulation_lifespan=1200,
        display_novelty=False,
        save_archive=True,
        show_gui=True
    )

    # Novelty Search through Genetic Evolution
    archive = evolve(config=novelty_config, heterogeneous=True)

    results_config = ConfigurationDefaults.RESULTS
    results_config.world = world_config
    results_config.archive = archive

    # Take Results from Evolution, reduce dimensionality, and present User with Clusters.
    report(config=results_config, heterogeneous=True)

if __name__ == "__main__":
    simulate_from_single_controller()
    # evolve_heterogeneity()
