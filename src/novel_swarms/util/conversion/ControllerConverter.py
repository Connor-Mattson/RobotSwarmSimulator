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

class DiffDriveToRatio(ControllerConverter):
    """
    Takes controllers of the Form: [v_l0, vr_0, vl_1, vr_1] and converts it into a ratio?
    """
    def __init__(self, controller):
        super().__init__(controller)

    def convert(self):
        output = []
        assert len(self.from_controller) == 4
        v_r, v_l = self.from_controller[2], self.from_controller[3]
        v_on = (v_r + v_l) / 2
        dtheta_on = (v_r - v_l) / 7

        v_r, v_l = self.from_controller[0], self.from_controller[1]
        v_off = (v_r + v_l) / 2
        dtheta_off = (v_r - v_l) / 7
        return [dtheta_on / dtheta_off, v_on / v_off]

if __name__ == "__main__":
    wheel_radius = 4.1
    agent_radius = 15.1 / 2
    input_controller = [0.65, 1.0, 0.4, 0.5]
    SCALE = 4.5
    input_controller = [i * SCALE for i in input_controller]

    converter = DiffDriveToUnicycle(input_controller, agent_radius, wheel_radius)
    print(converter.convert())