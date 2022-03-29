"""File to test the state switcher that will determine our current state in function of the controller inputs."""
from ..controllers import Controller
from ..utils import state_switcher


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


def test_switcher_x_button():
    """If the controller is connected and the button Y is pressed, then stop."""
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
