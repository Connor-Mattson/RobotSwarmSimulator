"""
This class defines a configuration for how the World will output a large numpy array representing the
pixels on the screen
"""


class OutputTensorConfig:
    """
    :param screen: This is the screen
    """
    def __init__(self,
                 screen=None,
                 total_frames=5,
                 steps_between_frames=4,
                 timeless=False,
                 ):
        self.screen = screen
        self.total_frames = total_frames
        self.step = steps_between_frames
        self.timeless = timeless