"""State switcher class that will be used in the main control loop."""


class StateSwitcher:
    """State switcher class."""

    def __init__(self, memory):
        """Init of the class.

        Args:
            memory (dict): memory object.
        """
        self.memory = memory
        self.states = ["stop", "autonomous", "collect", "manual"]
        self.state = "driving"

    def update(self):
        """Update state using controller buttons."""
        controller_inp = self.memory.get('controller', {})

        if controller_inp == {} or controller_inp['button_y']:
            self.state = self.states[0]

        elif controller_inp['button_a']:
            self.state = self.states[2]

        elif (controller_inp['steering'] == 0.0 and controller_inp['throttle'] == 0.0):
            self.state = self.states[1]

        else:
            self.state = self.states[3]

        self.memory['state'] = self.state
