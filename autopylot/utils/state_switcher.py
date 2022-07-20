"""State switcher class that will be used in the main control loop."""
import json
import logging
import os

from ..utils import memory, settings


class StateSwitcher:
    """State switcher class."""

    def __init__(self, memory=memory.mem):
        """Init of the class.

        Args:
            memory (dict): memory object.
        """
        self.memory = memory
        self.states = ["stop", "collect", "manual", "autonomous"]
        self.state = self.states[0]

        self.actions = {
            # something like this
            "steering": "steering",
            "throttle": "throttle",
            "collect": "button_a",
            "manual": "button_x",
            "stop": "button_y",
        }
        self.load_custom_mapping()

        self.memory["state"] = self.state
        logging.info("Instantiated StateSwitcher.")

    def load_custom_mapping(self, filepath=settings.settings.ACTIONS_MAPPING_PATH):
        """
        Load a custom key buttons and axes to actions mapping from file.
        """
        if os.path.exists(filepath):
            mapping_dict = json.load(open(filepath))
            self.actions.update(mapping_dict)

            logging.info("Loaded custom actions mapping")

    def update(self):
        """Update state using controller buttons."""
        controller_inp = self.memory.get("controller", {})

        if controller_inp == {} or controller_inp.get(self.actions["stop"]):
            self.state = self.states[0]

        elif controller_inp.get(self.actions["collect"]):
            self.state = self.states[1]

        elif (
            controller_inp.get(self.actions["manual"])
            or controller_inp.get(self.actions["steering"]) != 0.0
            or controller_inp.get(self.actions["throttle"]) != 0.0
        ):
            self.state = self.states[2]

        else:
            self.state = self.states[3]

        if self.memory["state"] != self.state:
            self.memory["state"] = self.state
            logging.debug(f"State changed to: {self.state}")
