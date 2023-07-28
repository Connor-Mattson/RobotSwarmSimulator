import numpy as np

from src.novel_swarms.behavior.TotalCollisions import TotalCollisionsBehavior
from src.novel_swarms.config.AgentConfig import MazeAgentConfig, ModeSwitchingAgentConfig
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig
from src.novel_swarms.sensors.BinaryFOVSensor import BinaryFOVSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.world.simulate import main as sim

def get_mode_switching_keyboard(controllers):
    SEED = None
    GUI_PADDING = 15
    BL = 15.1
    N_AGENTS = 16
    WIDTH, HEIGHT = 1000, 1000

    sensors = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(BL * 13.25),
            bias=0,
            degrees=True,
            false_positive=0.0,
            false_negative=0.0,
            # Rectangle Representing Environment Boundaries
            walls=None,
            wall_sensing_range=(BL * 4),
            time_step_between_sensing=1,
            goal_sensing_range=(BL * 29.13),
            detect_goal_with_added_state=True,
        )
    ])

    agent_maze = MazeAgentConfig(
        controller=None,
        agent_radius=BL / 2,
        # dt=0.13,  # 130ms sampling period
        dt=0.13,
        sensors=sensors,
        seed=SEED,
        idiosyncrasies=False,
        body_filled=True,
        body_color=(255, 0, 0),
        stop_at_goal=False,
    )

    agent_mode_switching = ModeSwitchingAgentConfig(
        parent_config=agent_maze,
        controllers=controllers,
        switch_mode="Keyboard",
    )

    G = []
    objects = []
    behavior = [TotalCollisionsBehavior()]

    world_config = RectangularWorldConfig(
        size=(WIDTH, HEIGHT),
        n_agents=N_AGENTS,
        seed=SEED,
        behavior=behavior,
        show_walls=False,
        collide_walls=False,
        agent_initialization=[(500, 500, 0) for i in range(N_AGENTS)],
        agentConfig=agent_mode_switching,
        padding=15,
        objects=objects,
        goals=G,
        stop_at=None,
    )

    return world_config

if __name__ == "__main__":
    c = [
        [12.5, 0.5, 12.5, -0.5],
        [4.5, -0.2, -3.0, -0.2],
    ]
    w = get_mode_switching_keyboard(c)
    sim(w, show_gui=True, world_key_events=True)