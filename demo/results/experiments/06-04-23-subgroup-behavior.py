from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.EvolutionaryConfig import GeneticEvolutionConfig
from src.novel_swarms.config.HeterogenSwarmConfig import HeterogeneousSwarmConfig
from src.novel_swarms.config.defaults import ConfigurationDefaults
from src.novel_swarms.novelty.GeneRule import GeneBuilder, GeneRule
from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.novelty.evolve import main as evolve
from src.novel_swarms.results.results import main as report
from src.novel_swarms.behavior import *


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
        GeneRule(discrete_domain=[0.1, 0.2, 0.25, 0.33, 0.5], step_size=2, allow_mutation=True)
    ]
)

def display_subgroup_behaviors(c=None):
    if c is None:
        c = [-1.0, 1.0, 0.3, 0.2, 0.3, -0.9, 0.4, 1.0, 0.4]
        # c = [0.6, 0.7, 0.95, 0.95, 0.7, 0.8, 0.8, 0.7, 0.01]
    n = 24

    agent_A = DiffDriveAgentConfig(controller=None, sensors=ConfigurationDefaults.SIMPLE_SENSOR, dt=1.0, body_color=(255, 0, 0), body_filled=True)
    agent_B = DiffDriveAgentConfig(controller=None, sensors=ConfigurationDefaults.SIMPLE_SENSOR, dt=1.0, body_color=(0, 255, 0), body_filled=True)

    h_config = HeterogeneousSwarmConfig()
    h_config.add_sub_populuation(agent_A, n // 2)
    h_config.add_sub_populuation(agent_B, n // 2)
    h_config.from_n_species_controller(c)

    world = ConfigurationDefaults.RECTANGULAR_WORLD
    world.agentConfig = h_config
    world.behavior = [
        SubGroupBehavior(AverageSpeedBehavior(), subgroup=0),
        SubGroupBehavior(AngularMomentumBehavior(), subgroup=0),
        SubGroupBehavior(RadialVarianceBehavior(), subgroup=0),
        SubGroupBehavior(ScatterBehavior(), subgroup=0),
        SubGroupBehavior(GroupRotationBehavior(), subgroup=0),
        SubGroupBehavior(AverageSpeedBehavior(), subgroup=1),
        SubGroupBehavior(AngularMomentumBehavior(), subgroup=1),
        SubGroupBehavior(RadialVarianceBehavior(), subgroup=1),
        SubGroupBehavior(ScatterBehavior(), subgroup=1),
        SubGroupBehavior(GroupRotationBehavior(), subgroup=1),
    ]
    world.collide_walls = True
    world.show_walls = True
    h_config.attach_world_config(world)

    w = sim(world, show_gui=True, step_size=5)
    return w

def display_random_behaviors(n):
    for _ in range(n):
        c = SINGLE_SENSOR_HETEROGENEOUS_MODEL.fetch_random_genome()
        display_subgroup_behaviors(c)

if __name__ == "__main__":
    # display_subgroup_behaviors()
    display_random_behaviors(500)