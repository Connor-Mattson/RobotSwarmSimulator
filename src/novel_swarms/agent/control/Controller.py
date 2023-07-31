class Controller:
    """
    Given agent observations, return agent actions
    """
    def __init__(self, controller):
        """
        Controllers can take two forms
        First, a list of values where n states are mapped to n * k outputs, where k is the number of output values per state
        Second, a function, that takes an agent as an argument, and returns the appropriate k values based on the agent information.
        """

        self.controller_as_list = None
        self.controller_as_method = None

        # Case 1: Controller is a Python List
        if isinstance(controller, list):
            self.list_based = True
            self.controller_as_list = controller

        # Case 2: Controller is a Python Function
        elif callable(controller):
            self.list_based = False
            self.controller_as_method = controller

        # Neither --> Error
        else:
            raise Exception("The input value of controller to class Controller must be a callable or a list!")

    def get_actions(self, agent):
        if self.list_based:
            sensor_state = agent.sensors.getState()
            e1 = self.controller_as_list[sensor_state * 2]
            e2 = self.controller_as_list[(sensor_state * 2) + 1]
            return e1, e2
        else:
            return self.controller_as_method(agent)

