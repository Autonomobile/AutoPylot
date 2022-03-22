from ..utils import memory, settings
from .serial_control import SerialControl
from .sim_control import SimControl


def Control(
    memory=memory.mem,
    control_type=settings.settings.CONTROL_TYPE,
    *args,
    **kwargs,
):
    if control_type == "serial":
        return SerialControl(memory=memory, *args, **kwargs)
    elif control_type == "sim":
        return SimControl(memory=memory, *args, **kwargs)
    else:
        raise ValueError(f"Unknown control type {control_type}")
