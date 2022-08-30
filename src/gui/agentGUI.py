import pygame
from src.agent.DiffDriveAgent import DifferentialDriveAgent
from src.gui.abstractGUI import AbstractGUI
from src.world.World import World


class DifferentialDriveGUI(AbstractGUI):
    # Pair the GUI to the World
    world = None
    title = None
    subtitle = None
    selected = None
    text_baseline = 10

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x=x, y=y, w=w, h=h)

    def set_selected(self, agent: DifferentialDriveAgent):
        super().set_selected(agent)
        self.selected = agent

    def set_title(self, title, subtitle=None):
        self.title = title
        self.subtitle = subtitle

    def set_world(self, world: World):
        self.world = world

    def draw(self, screen):
        super().draw(screen)
        self.text_baseline = 10
        if pygame.font:
            if self.title:
                self.appendTextToGUI(screen, self.title, size=20)
            if self.subtitle:
                self.appendTextToGUI(screen, self.subtitle, size=18)
            if self.selected:
                a = self.selected
                self.appendTextToGUI(screen, f"Current Agent: {a.name}")
                self.appendTextToGUI(screen, f"")
                self.appendTextToGUI(screen, f"x: {a.x_pos}")
                self.appendTextToGUI(screen, f"y: {a.y_pos}")
                self.appendTextToGUI(screen, f"dx: {a.dx}")
                self.appendTextToGUI(screen, f"dy: {a.dy}")
                self.appendTextToGUI(screen, f"")
                self.appendTextToGUI(screen, f"VR 0: {a.vr_0}")
                self.appendTextToGUI(screen, f"VL 0: {a.vl_0}")
                self.appendTextToGUI(screen, f"VR 1: {a.vr_1}")
                self.appendTextToGUI(screen, f"VL 1: {a.vl_1}")
                self.appendTextToGUI(screen, f"")
                self.appendTextToGUI(screen, f"θ: {a.angle}")
                if a.agent_in_sight is not None:
                    self.appendTextToGUI(screen, f"sees: {a.agent_in_sight.name}")
            else:
                self.appendTextToGUI(screen, "Current Agent: None")
                self.appendTextToGUI(screen, "")
                self.appendTextToGUI(screen, "Behavior", size=18)
                for b in self.world.behavior:
                    out = b.out_average()
                    self.appendTextToGUI(screen, "{} : {:0.2f}".format(out[0], out[1]))

        else:
            print("NO FONT")

    def appendTextToGUI(self, screen, text, x=None, y=None, color=(255, 255, 255), aliasing=True, size=16):

        if not x:
            x = self.x + 10
        if not y:
            y = self.text_baseline

        font = pygame.font.Font(None, size)
        text = font.render(text, aliasing, color)
        textpos = (x, y)
        screen.blit(text, textpos)
        self.text_baseline += size + 1
