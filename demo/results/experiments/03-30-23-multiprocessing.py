from multiprocessing import Pool
from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.util import Timer
from src.novel_swarms.util import MultiWorldSimulation
import matplotlib.pyplot as plt


def stop_detection_method(world):
    EPSILON = 0.001
    if world.total_steps > 100 and world.behavior[2].out_average()[1] < EPSILON:
        return True
    return False

def simulate(agent_config, show_gui=False):
    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=30,
        seed=1,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        stop_at=1000,
    )

    world = sim(world_config, show_gui=show_gui)
    # print([b.out_average()[1] for b in world.behavior])
    return world.behavior[2].out_average()[1]

def compare_approaches():
    agent_configs = []
    for i in range(-10, 11, 5):
        for j in range(-10, 11, 5):
            controller = [i * 0.1, j * 0.1, 1.0, 1.0]
            sensors = SensorSet([
                BinaryLOSSensor(angle=0),
            ])
            agent_config = DiffDriveAgentConfig(
                controller=controller,
                sensors=sensors,
                seed=1,
            )
            agent_configs.append(agent_config)

    time_it = Timer("Multi-processing")
    with Pool(12) as p:
        ret = p.map(simulate, agent_configs)
        print(ret)
    multi_time = time_it.stop_the_clock()

    time_it = Timer("Single-Processing-No-GUI")
    for a_config in agent_configs:
        simulate(a_config)
    single_time_no_gui = time_it.stop_the_clock()

    time_it = Timer("Single-Processing-With-GUI")
    for a_config in agent_configs:
        simulate(a_config, show_gui=True)
    single_time_with_gui = time_it.stop_the_clock()

    print(f"Results for {len(agent_configs)} controllers")
    print(f"Multiprocessing Time... {multi_time}s")
    print(f"Iterating Without GUI... {single_time_no_gui}")
    print(f"Iterating With GUI... {single_time_with_gui}")

def plot_findings():
    data = {"Single-Thread w/GUI" : 252.02, "Single-Thread no GUI" : 45.91, "Multiprocessing (12 threads)" : 6.14}
    labels = data.keys()
    values = data.values()

    fig = plt.figure(figsize=(10, 5))

    plt.bar(labels, values, color='blue')
    plt.ylabel("Time (s)")
    plt.title("Time to Simulate 25 controllers for 30 agents for 1000 timesteps")
    plt.show()

def object_oriented_approach():
    controllers = [[i * 0.1, j * 0.1, 1.0, 1.0] for i in range(-10, 11, 10) for j in range(-10, 11, 10)]
    agent_config = [
        DiffDriveAgentConfig(
            controller=controller,
            sensors=SensorSet([
                BinaryLOSSensor(angle=0),
            ]),
            seed=1,
        ) for controller in controllers
    ]
    sim_config = [
        RectangularWorldConfig(
            size=(500, 500),
            n_agents=30,
            seed=1,
            behavior=[
                AverageSpeedBehavior(),
                AngularMomentumBehavior(),
                RadialVarianceBehavior(),
                ScatterBehavior(),
                GroupRotationBehavior(),
            ],
            agentConfig=a_c,
            padding=15,
            stop_at=2500,
        ) for a_c in agent_config
    ]

    processor = MultiWorldSimulation(pool_size=12, single_step=True, with_gui=True)
    time_it = Timer("Full 21x21 search for cyclic")
    ret = processor.execute(sim_config, world_stop_condition=stop_detection_method)
    print([r.total_steps for r in ret])
    time_it.check_watch()

if __name__ == "__main__":
    object_oriented_approach()


