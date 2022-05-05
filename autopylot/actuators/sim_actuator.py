from ..utils import memory, sim_client


class SimActuator:
    def __init__(
        self,
        client=sim_client.client,
        memory=memory.mem,
        steering_key="steering",
        throttle_key="throttle",
        speed_key="speed",
    ):
        self.__client = client
        self.__memory = memory

        self.__steering_key = steering_key
        self.__throttle_key = throttle_key
        self.__speed_key = speed_key
        self.__steering = 0
        self.__throttle = 0

        self.__memory[self.__speed_key] = 0.0

    def apply_steering(self, steering):
        """Change steering.

        Args:
            steering (float): steering between -1 and 1.
        """
        self.__steering = steering
        self.__client.send_controls(self.__steering, self.__throttle)

    def apply_throttle(self, throttle):
        """Change motor throttle.

        Args:
            throttle (float): throttle between -1 and 1.
        """
        self.__throttle = throttle
        self.__client.send_controls(self.__steering, self.__throttle)

    def apply_steering_throttle(self, steering, throttle):
        """Change all the elements at the same time.

        Args:
            steering (float): steering between -1 and 1.
            throttle (float): throttle between -1 and 1.
        """
        self.__steering = steering
        self.__throttle = throttle
        self.__client.send_controls(self.__steering, self.__throttle)

    def update(self):
        """Update steering and throttle using memory."""
        steering = self.__memory.get(self.__steering_key, 0)
        throttle = self.__memory.get(self.__throttle_key, 0)
        self.apply_steering_throttle(steering, throttle)
        self.__memory[self.__speed_key] = self.__client.speed / 8.0

    def get_sensor_last_received(self):
        return self.client.last_received
