class ControllerConverter:
    def __init__(self, controller):
        self.from_controller = controller

    def convert(self):
        pass


class DiffDriveToUnicycle(ControllerConverter):
    """
    Takes controllers of the Form: [v_l0, vr_0, vl_1, vr_1] and converts it to the unicycle controller: [v_0, w_0, v_1, w_1]
    """
    def __init__(self, controller, agent_radius, wheel_radius):
        super().__init__(controller)
        self.a_rad = agent_radius
        self.w_rad = wheel_radius

    def convert(self):
        output = []
        assert len(self.from_controller) % 2 == 0
        for i in range(0, len(self.from_controller), 2):
            v_l = self.from_controller[i]
            v_r = self.from_controller[i + 1]
            forward_velocity = (self.w_rad / 2) * (v_l + v_r)
            d_theta = (v_l - v_r) / (2 * self.a_rad)
            output.append(forward_velocity)
            output.append(d_theta)
        return output


if __name__ == "__main__":
    wheel_radius = 2.0
    agent_radius = 5.0
    input_controller = [-0.7, -1.0, 1.0, -1.0]

    converter = DiffDriveToUnicycle(input_controller, agent_radius, wheel_radius)
    print(converter.convert())