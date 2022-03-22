# script based on https://github.com/autorope/donkeycar/blob/dev/donkeycar/parts/controller.py

from ..utils import memory, settings
from .joystick import XboxOneJoystick
from .keyboard import Keyboard


def Controller(
    memory=memory.mem,
    controller_type=settings.settings.CONTROLLER_TYPE,
    *args,
    **kwargs,
):
    if controller_type == "xbox":
        return XboxOneJoystick(memory=memory, *args, **kwargs)
    elif controller_type == "keyboard":
        return Keyboard(memory=memory, *args, **kwargs)
    else:
        raise ValueError(f"Unknown controller type {controller_type}")
