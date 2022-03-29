from ..utils import memory, settings


def Actuator(
    memory=memory.mem,
    actuator_type=settings.settings.ACTUATOR_TYPE,
    *args,
    **kwargs,
):
    if actuator_type == "serial":
        from .serial_actuator import SerialActuator

        return SerialActuator(memory=memory, *args, **kwargs)
    elif actuator_type == "sim":
        from .sim_actuator import SimActuator

        return SimActuator(memory=memory, *args, **kwargs)
    else:
        raise ValueError(f"Unknown actuator type {actuator_type}")
