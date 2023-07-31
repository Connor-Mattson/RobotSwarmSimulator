from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.gui.controllerGUI import ControllerGUI

def simulate_and_report():
    # CYCLIC_PURSUIT_CONTROLLER = [-0.7, 0.3, 1.0, 1.0]
    CYCLIC_PURSUIT_CONTROLLER = [0.7, 1.0, 0.4, 0.5]
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
        n_agents=20,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        collide_walls=True,
        show_walls=True,
    )

    gui = ControllerGUI(world_config.w, 0, 200, world_config.h)

    simulate(world_config=world_config, gui=gui, world_key_events=False, gui_key_events=True)


if __name__ == "__main__":
    hist = simulate_and_report()
    # hist = np.array([0.0003708610280283855, 0.0002170609370835147, 0.00022681563223493154, 0.00010145147013828387, 8.367161149181384e-05, 6.1229413697511e-05, 5.682383435089836e-05, 1.7797777344077795e-05, 1.886204297308302e-05, 1.2412422508310492e-05, 2.411153886067053e-05, 3.260565484999294e-05, 1.2755020587553701e-05, 6.426228318429122e-05, 0.0017108039413167965, 0.012492167327887015, 0.008570446029409333, 0.007077810625387572, 0.004915499711902706, 0.005642383628653594])
