from ..utils import memory, settings
from .serial_actuator import SerialActuator
from .sim_actuator import SimActuator


def Actuator(
    memory=memory.mem,
    actuator_type=settings.settings.ACTUATOR_TYPE,
    *args,
    **kwargs,
):
    if actuator_type == "serial":
        return SerialActuator(memory=memory, *args, **kwargs)
    elif actuator_type == "sim":
        return SimActuator(memory=memory, *args, **kwargs)
    else:
        raise ValueError(f"Unknown actuator type {actuator_type}")
