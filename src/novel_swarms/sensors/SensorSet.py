import warnings


class SensorSet:
    def __init__(self, sensors=None, custom_state_decision=None):
        if sensors is None or len(sensors) == 0:
            warnings.warn("No Sensor Data was provided to the Sensor Set. Agents will likely perform trivial behaviors")
        self.sensors = sensors
        self.custom_state_decision = custom_state_decision

    def __iter__(self):
        for sensor in self.sensors:
            yield sensor

    def __index__(self, i):
        return self.sensors[i]

    def __len__(self):
        return len(self.sensors)

    def getState(self):
        """
        If no method for state is provided at init, assume the decision tree is full and binary w.r.t. the controller.
        Controller of size n (n/2 pairwise wheel velocities) then the decision space is 2^(n-1), by default.
        """
        if self.custom_state_decision is None:
            binary_states = [str(sensor.current_state) for sensor in self.sensors]
            state = int(''.join(binary_states), 2)
            return state
        else:
            sensor_states = [sensor.current_state for sensor in self.sensors]
            state = self.custom_state_decision(sensor_states)
            return state

    def getDetectionId(self):
        return max([sensor.detection_id for sensor in self.sensors])

    def getStatePermutationSize(self):
        return sum([s.n_possible_states for s in self.sensors])


