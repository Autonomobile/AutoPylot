import keyboard

from ..utils import memory


class Keyboard:
    """Keyboard controller (mainly debugging purpose)."""

    def __init__(self, memory=memory.mem, *args, **kwargs):
        self.memory = memory

        self.keys_to_steer = {
            "q": -1,
            "z": 0,
            "d": 1,
        }
        self.bkeys = ["s"]
        self.key_recording = "r"

    def update(self):
        """Update function for the keyboard controller.
        This function stores in the memory the newly fetched keyboard inputs.
        """
        pressed = []
        bpressed = []
        for k in self.keys_to_steer.keys():
            pressed.append(keyboard.is_pressed(k))
        for bk in self.bkeys:
            bpressed.append(keyboard.is_pressed(bk))

        sum_steer = 0
        count = 0
        for key, k_pressed in zip(self.keys_to_steer.keys(), pressed):
            if k_pressed:
                sum_steer += self.keys_to_steer[key]
                count += 1

        if count != 0:
            steering = sum_steer / count
            throttle = 0.5

        else:
            steering = 0
            throttle = 0

        if any(bpressed):
            throttle *= -1

        self.memory["controller"] = {
            "steering": steering,
            "throttle": throttle,
            "button_a": keyboard.is_pressed(self.key_recording),
            "button_x": any(pressed),
        }
