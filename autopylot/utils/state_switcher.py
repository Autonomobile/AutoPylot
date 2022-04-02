"""State switcher class that will be used in the main control loop."""
import logging

from ..utils import memory


class StateSwitcher:
    """State switcher class."""

    def __init__(self, memory=memory.mem):
        """Init of the class.

        Args:
            memory (dict): memory object.
        """
        self.memory = memory
        self.states = ["stop", "autonomous", "collect", "manual"]
        self.state = self.states[0]

        self.memory["state"] = self.state
        logging.info("Instantiated StateSwitcher.")

    def update(self):
        """Update state using controller buttons."""
        controller_inp = self.memory.get("controller", {})

        if controller_inp == {}:
            self.state = self.states[0]

        elif controller_inp["button_a"]:
            self.state = self.states[2]

        elif (
            controller_inp["button_x"]
            or controller_inp["steering"] != 0.0
            or controller_inp["throttle"] != 0.0
        ):
            self.state = self.states[3]

        else:
            self.state = self.states[1]

        if self.memory["state"] != self.state:
            logging.debug(f"State changed to: {self.state}")
            self.memory["state"] = self.state
