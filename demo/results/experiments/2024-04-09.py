"""
DO NOT ALTER THIS FILE.
This file should remain a constant reference to a specific behavior.
Please create your own file for simulating or alter 'demo/simulation/playground.py' instead.
"""
import pygame
import random
from src.novel_swarms.world.simulate import main as simulate
from src.novel_swarms.behavior.AngularMomentum import AngularMomentumBehavior
from src.novel_swarms.behavior.AverageSpeed import AverageSpeedBehavior
from src.novel_swarms.behavior.GroupRotationBehavior import GroupRotationBehavior
from src.novel_swarms.behavior.RadialVariance import RadialVarianceBehavior
from src.novel_swarms.behavior.ScatterBehavior import ScatterBehavior
from src.novel_swarms.sensors.BinaryLOSSensor import BinaryLOSSensor
from src.novel_swarms.sensors.SensorSet import SensorSet
from src.novel_swarms.config.AgentConfig import DiffDriveAgentConfig
from src.novel_swarms.config.WorldConfig import PhysicsRectangularWorldConfig
from src.novel_swarms.world.objects.Puck import Puck

if __name__ == "__main__":

    CYCLIC_PURSUIT_CONTROLLER = [-0.7, -1.0, 1.0, -1.0]
    SEED = 1

    sensors = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    agent_config = DiffDriveAgentConfig(
        controller=CYCLIC_PURSUIT_CONTROLLER,
        sensors=sensors,
        seed=SEED,
    )

    behavior = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    world_config = PhysicsRectangularWorldConfig(
        size=(500, 500),
        n_agents=20,
        seed=SEED,
        behavior=behavior,
        agentConfig=agent_config,
        padding=15,
        objects=[
            Puck(250 + random.random(), 250 + random.random(), 8, pygame.Color("red")) for _ in range(200)
        ]
    )

    simulate(world_config=world_config, save_duration=2000, save_every_ith_frame=5, save_time_per_frame=20)
