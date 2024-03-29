"""File to test the state switcher that will determine our current state in function of the controller inputs."""
import os
import json

from ..controllers import Controller
from ..utils import state_switcher, settings


def test_switcher_stop_empty():
    """If the memory is empty, then stop."""
    mem = {}

    sw = state_switcher.StateSwitcher(mem)
    sw.update()

    assert mem["state"] == "stop"


def test_switcher_stop_disconnected():
    """If the controller is not connected, then stop."""
    mem = {}

    js = Controller(mem, controller_type="xbox", do_init=False)
    sw = state_switcher.StateSwitcher(mem)

    js.update()
    sw.update()

    assert mem["state"] == "stop"


def test_switcher_stop_button():
    """If the controller is connected and the button Y is pressed, then stop."""
    mem = {
        "controller": {
            "steering": 0.2,
            "throttle": 0.1,
            "button_y": True,
            "button_x": True,
            "button_a": False,
        }
    }

    sw = state_switcher.StateSwitcher(mem)
    sw.update()

    assert mem["state"] == "stop"


def test_switcher_x_button():
    """If the controller is connected and the button X is pressed, then manual."""
    mem = {
        "controller": {
            "steering": 0.2,
            "throttle": 0.1,
            "button_x": True,
            "button_a": False,
        }
    }

    sw = state_switcher.StateSwitcher(mem)
    sw.update()

    assert mem["state"] == "manual"


def test_switcher_autonomous():
    """If the controller is connected and both the steering and throttle are 0.0, then autonomous."""
    mem = {
        "controller": {
            "steering": 0.0,
            "throttle": 0.0,
            "button_x": False,
            "button_a": False,
        }
    }

    sw = state_switcher.StateSwitcher(mem)
    sw.update()

    assert mem["state"] == "autonomous"


def test_switcher_collect():
    """If the controller is connected and the button A is pressed, then collect."""
    mem = {
        "controller": {
            "steering": 0.0,
            "throttle": 0.0,
            "button_x": False,
            "button_a": True,
        }
    }

    sw = state_switcher.StateSwitcher(mem)
    sw.update()

    assert mem["state"] == "collect"


def test_switcher_manual():
    """If the controller is connected and both button Y and A are not pressed, then manual (no collect)."""
    mem = {
        "controller": {
            "steering": 0.2,
            "throttle": 0.1,
            "button_x": False,
            "button_a": False,
        }
    }

    sw = state_switcher.StateSwitcher(mem)
    sw.update()

    assert mem["state"] == "manual"


def test_switcher_custom_mapping():
    mem = {
        "controller": {
            "steering": 0.2,
            "throttle": 0.1,
            "button_x": True,
            "button_a": False,
            "button_b": True,
        }
    }
    custom_mapping = {"stop": "button_b"}
    filepath = os.path.join(
        settings.settings.ROOT_PATH, "test_switcher_custom_mapping.json"
    )
    with open(filepath, "w") as f:
        json.dump(custom_mapping, f, indent=4)
    assert os.path.exists(filepath)

    sw = state_switcher.StateSwitcher(mem)
    sw.load_custom_mapping(filepath)
    assert sw.actions["stop"] == "button_b"

    sw.update()
    assert mem["state"] == "stop"

    os.remove(filepath)
