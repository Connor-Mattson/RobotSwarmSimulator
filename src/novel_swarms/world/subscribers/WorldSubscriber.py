
class WorldSubscriber:
    def __init__(self, func):
        """
        Params
        - func: A function with two parameters (world, screen) that will be called upon notification
        """
        self.func = func

    def notify(self, world, screen):
        """
        Call self.func everytime the subscriber is notified
        """
        self.func(world, screen)