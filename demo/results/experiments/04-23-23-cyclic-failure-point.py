from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
import matplotlib.pyplot as plt
import numpy as np

def simulate_and_report():
    CYCLIC_PURSUIT_CONTROLLER = [-0.7, 0.3, 1.0, 1.0]
    SEED = 3

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=CYCLIC_PURSUIT_CONTROLLER,
        sensors=sensors,
        seed=SEED,
        agent_radius=7
    )

    behavior = [
        RadialVarianceBehavior()
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        collide_walls=True,
        show_walls=True,
    )

    hist = []

    def remove_agents(world):
        if world.total_steps > 2500 and world.total_steps % 2000 == 0:
            hist.append(world.behavior[0].out_average()[1])
            world.removeAgent(world.population[-1])
            if len(world.population) < 5:
                return True
        return False

    simulate(world_config=world_config, world_key_events=True, stop_detection=remove_agents)
    print(hist)
    return hist

def graph(data):
    x = range(24 - 4)
    x_labels = range(24, 4, -1)
    plt.plot(data)
    plt.xticks(x, x_labels)
    plt.title("Resilience of Cycic Pursuit Swarm As Agents are Removed")
    plt.ylabel("Cycle Error (Radial Variance)")
    plt.xlabel("no. Agents after removal")
    plt.show()

if __name__ == "__main__":
    hist = simulate_and_report()
    # hist = np.array([0.0003708610280283855, 0.0002170609370835147, 0.00022681563223493154, 0.00010145147013828387, 8.367161149181384e-05, 6.1229413697511e-05, 5.682383435089836e-05, 1.7797777344077795e-05, 1.886204297308302e-05, 1.2412422508310492e-05, 2.411153886067053e-05, 3.260565484999294e-05, 1.2755020587553701e-05, 6.426228318429122e-05, 0.0017108039413167965, 0.012492167327887015, 0.008570446029409333, 0.007077810625387572, 0.004915499711902706, 0.005642383628653594])
    graph(hist)
