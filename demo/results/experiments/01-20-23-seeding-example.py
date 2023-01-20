
import random
from novel_swarms.config.WorldConfig import RectangularWorldConfig
from novel_swarms.world.WorldFactory import WorldFactory
from novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from novel_swarms.sensors.SensorSet import SensorSet
from novel_swarms.config.AgentConfig import DiffDriveAgentConfig

def test_A():
    SEED = 1
    random.seed(SEED)
    positions = []
    for i in range(29):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        positions.append((x, y))
    print(positions)

def test_B():
    SEED = 1

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        sensors=sensors,
        trace_length=160,
        body_color="Random",
        body_filled=True,
    )

    world_config = RectangularWorldConfig(
        size=(500, 500),
        n_agents=24,
        seed=SEED,
        agentConfig=agent_config,
        padding=15,
    )

    world = WorldFactory.create(world_config)
    print([(a.x_pos, a.y_pos, a.angle) for a in world.population])


if __name__ == "__main__":
    # test_A()
    test_B()