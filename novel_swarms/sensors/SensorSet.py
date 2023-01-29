import warnings


class SensorSet:
    def __init__(self, sensors=None):
        if sensors is None or len(sensors) == 0:
            warnings.warn("No Sensor Data was provided to the Sensor Set. Agents will likely perform trivial behaviors")
        self.sensors = sensors

    def __iter__(self):
        for sensor in self.sensors:
            yield sensor

    def __index__(self, i):
        return self.sensors[i]

    def __len__(self):
        return len(self.sensors)

    def getState(self):
        """
        Currently only works with binary sensors.
        """
        binary_states = [str(sensor.current_state) for sensor in self.sensors]
        state = int(''.join(binary_states), 2)
        return state

    def getDetectionId(self):
        return max([sensor.detection_id for sensor in self.sensors])

    def getStatePermutationSize(self):
        return sum([s.n_possible_states for s in self.sensors])


