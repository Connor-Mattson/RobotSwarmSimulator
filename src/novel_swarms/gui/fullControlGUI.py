import pygame
from ..agent.DiffDriveAgent import DifferentialDriveAgent
from .abstractGUI import AbstractGUI
from ..world.World import World
import numpy as np
import thorpy as tp


class FullControlGUI(AbstractGUI):
    # Pair the GUI to the World
    world = None
    title = None
    subtitle = None
    selected = None
    text_baseline = 10

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x=x, y=y, w=w, h=h)
        self.rec = pygame.Rect((x, y), (w, h))
        self.track_all_events = True
        self.track_all_mouse = True

    def set_selected(self, agent: DifferentialDriveAgent):
        super().set_selected(agent)
        self.selected = agent

    def set_title(self, title, subtitle=None):
        self.title = title
        self.subtitle = subtitle

    def set_world(self, world: World):
        self.world = world

    def set_time(self, time_steps):
        self.time = time_steps

    def recieve_events(self, events):
        super().recieve_events(events)
        self.events = events

    def recieve_mouse(self, mouse_rel):
        super().recieve_mouse(mouse_rel)
        self.mouse_rel = mouse_rel

    def set_screen(self, screen):
        super().set_screen(screen)

        # Declare a subsurface where the drawing will take place
        self.subsurf = self.screen.subsurface(self.rec)
        tp.init(self.screen, tp.theme_human) #bind screen to gui elements and set theme
        tp.set_default_font(("arialrounded", "arial", "calibri", "century"), font_size=9)
        tp.set_style_attr("font_size", 12)
        self.init_gui_elements()


    def emit(event_name):
        pass

    def click_play():
        pass

    def init_gui_elements(self):
        play_button = tp.Button("Play")
        next_frame = tp.Button("Next Frame")
        speed_up = tp.Button("Speed -")
        speed_down = tp.Button("Speed +")

        some_buttons = [
            play_button,
            next_frame,
            speed_up,
            speed_down
        ]

        # some_buttons.append(tp.Text("Try hovering the bottom right angle of the box to resize it."))

        for button in some_buttons:
            button.set_font_size(12)
       
        self.box = tp.Box(some_buttons)
        self.box.sort_children("grid", nx=3, ny=1)
        # self.box.sort_children(margins=(40,40)) #use large margin so we can test negative resize easily
        # self.box.set_resizable(True, True)
        self.box.center_on(self.rec)
        self.box_updater = self.box.get_updater()

    def draw(self, screen):
        super().draw(screen)
        self.box_updater.update(events=self.events, mouse_rel=self.mouse_rel)
    
        
