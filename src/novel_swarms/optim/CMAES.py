import cma
import numpy as np

# class CMAES:
#     def __init__(self):
#         pass
    
def test_optim(x):
    return np.linalg.norm(np.array(x) - np.array([100, 20]))

def stop_detection_method(world):
    EPSILON = 0.001
    if world.total_steps > 100 and world.behavior[2].out_average()[1] < EPSILON:
        return True
    return False

def get_world(n, controller):
    from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
    from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
    from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
    from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
    from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
    from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
    from src.novel_swarms.sensors.SensorSet import SensorSet
    from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
    from src.novel_swarms.config.WorldConfig import RectangularWorldConfig


    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])
    agent_config = DiffDriveAgentConfig(
        controller=controller,
        sensors=sensors,
        seed=1,
    )
    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=n,
        seed=1,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        stop_at=1000,
    ) 
    return world_config

def simulator_optim(x):
    N = round(x[0])
    controller = x[1:]
    wc = get_world(N, controller)
    
    from src.novel_swarms.world.simulate import main as sim
    world = sim(wc, show_gui=True, stop_detection=stop_detection_method, step_size=10)
    return world.behavior[2].out_average()[1] + (world.total_steps / 1000)
    
def example_A():
    fun = test_optim  # we could use `functools.partial(cma.ff.elli, cond=1e4)` to change the condition number to 1e
    x0 = 2 * [2]  # initial solution
    sigma0 = 1    # initial standard deviation to sample new solutions

    xopt, es = cma.fmin2(fun, x0, sigma0, {'bounds': [[None, None], None]})
    return xopt, es

def example_B():
    fun = simulator_optim  # we could use `functools.partial(cma.ff.elli, cond=1e4)` to change the condition number to 1e

    # Decision Variables
    x0 = [10, 0.0, 0.0, 0.0, 0.0]
    sigma0 = 1    # initial standard deviation to sample new solutions
    lower_constraints = [2, -1, -1, -1, -1]
    upper_constraints = [30, 1, 1, 1, 1]

    xopt, es = cma.fmin2(fun, x0, sigma0, {'bounds': [lower_constraints, upper_constraints]})
    return xopt, es

if __name__ == "__main__":
    print(example_B())