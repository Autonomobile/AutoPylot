"""Joystick config."""

import json
import logging

from ..utils import settings
from .joystick import Joystick


def create_config(
    button_list=[
        "button_a",
        "button_b",
        "button_x",
        "button_y",
        "button_back",
        "button_start",
        "button_lb",
        "button_rb",
    ],
    axis_list=[
        "x",
        "y",
        "z",
        "rx",
        "ry",
        "rz",
        "hat0x",
        "hat0y",
        "hat1x",
        "hat1y",
    ],
):
    """Create a joystick config."""

    joy = Joystick()
    joy.init(config=True)

    if not joy.connected:
        logging.error("Joystick not connected.")
        return

    button_names = {}
    axis_names = {}

    for button in button_list:
        logging.info(f"Press button {button}")

        pressed_button = []
        done = False

        while not done:
            pressed_buttons, _ = joy.poll_raw()

            if len(pressed_buttons) == 1:
                button_names[pressed_buttons[0]] = button
                done = True
            else:
                logging.warning(f"More than one button pressed {pressed_button}")

    for axis in axis_list:
        logging.info(f"Use axis {axis}")

        pressed_axis = []
        done = False

        while not done:
            _, pressed_axis = joy.poll_raw()

            if len(pressed_axis) == 1:
                axis_names[pressed_axis[0]] = axis
                done = True

    # save the config
    with open(settings.settings.CONTROLLER_MAPPING_PATH, "w") as f:
        json.dump(
            {
                "axis_names": axis_names,
                "button_names": button_names,
            },
            f,
            indent=4,
        )
    logging.log(f"Saved joystick config to {settings.settings.CONTROLLER_MAPPING_PATH}")


if __name__ == "__main__":
    create_config()
