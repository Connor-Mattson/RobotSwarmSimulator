"""
This class defines a configuration for how the World will output a large numpy array representing the
pixels on the screen
"""


class OutputTensorConfig:
    def __init__(self,
                 screen=None,
                 total_frames=5,
                 steps_between_frames=4,
                 timeless=False,
                 colored=False,
                 background_color=(0,0,0)
                 ):
        self.screen = screen
        self.total_frames = total_frames
        self.step = steps_between_frames
        self.timeless = timeless
        self.colored = colored
        self.background_color = background_color
