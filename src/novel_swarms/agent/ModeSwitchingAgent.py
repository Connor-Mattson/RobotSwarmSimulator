import math
from ..agent.Agent import Agent
from ..config.AgentConfig import ModeSwitchingAgentConfig
from typing import Tuple
import pygame

class ModeSwitchingAgent(Agent):
    def __init__(self, config: ModeSwitchingAgentConfig = None, name=None):
        super().__init__(config.configs[0], name)

        # Create agents from config
        for c in config.configs:
            print(f"CONFIG: {c.as_dict()}")
        from ..agent.AgentFactory import AgentFactory
        self.agents = [AgentFactory.create(c) for c in config.configs]
        self.active_index = 0
        self.active = self.agents[self.active_index]
        self.radius = self.active.radius

        self.config_queue = config.configs
        self.switch_mode = config.switch_mode

    def step(self, check_for_world_boundaries=None, check_for_agent_collisions=None, world=None) -> None:
        super().step(check_for_world_boundaries)
        self.active.step(check_for_world_boundaries=check_for_world_boundaries, check_for_agent_collisions=check_for_agent_collisions, world=world)

    def draw(self, screen) -> None:
        super().draw(screen)
        self.active.draw(screen)

    def get_aabb(self):
        super().get_aabb()
        return self.active.get_aabb()

    def build_collider(self):
        return self.active.build_collider()

    def on_key_press(self, event):
        if self.switch_mode == "Keyboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.switch()

    def switch(self):
        old_agent = self.active
        new_agent = self.agents[self.active_index % len(self.agents)]

        # Copy Position, Orientation from old_agent to new_agent
        new_agent.set_x_pos(old_agent.get_x_pos())
        new_agent.set_y_pos(old_agent.get_y_pos())
        new_agent.set_heading(old_agent.get_heading())
        new_agent.name = old_agent.name

        self.active = new_agent
        self.active_index += 1


    def get_x_pos(self):
        return self.active.get_x_pos()

    def get_y_pos(self):
        return self.active.get_y_pos()

    def set_x_pos(self, new_x):
        return self.active.set_x_pos(new_x)

    def set_y_pos(self, new_y):
        return self.active.set_y_pos(new_y)

    def get_heading(self):
        return self.active.get_heading()

    def set_heading(self, new_heading):
        self.active.set_heading(new_heading)

    def get_sensors(self):
        return self.active.get_sensors()

    def set_name(self, new_name):
        self.name = new_name
        for a in self.agents:
            a.set_name(new_name)