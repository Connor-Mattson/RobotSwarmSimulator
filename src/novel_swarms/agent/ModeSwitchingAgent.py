import math
from src.novel_swarms.agent.MazeAgent import MazeAgent
from src.novel_swarms.config.AgentConfig import ModeSwitchingAgentConfig
from typing import Tuple
import pygame

class ModeSwitchingAgent(MazeAgent):
    def __init__(self, config: ModeSwitchingAgentConfig = None, name=None):
        super().__init__(config.parent_config, name)
        self.controller_set = config.controllers
        self.curr_controller = 0
        self.switch_mode = config.switch_mode
        self.set_controller()

    def on_key_press(self, event):
        if self.switch_mode == "Keyboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.curr_controller += 1
                    self.set_controller()

    def set_controller(self):
        self.controller = self.controller_set[self.curr_controller % len(self.controller_set)]