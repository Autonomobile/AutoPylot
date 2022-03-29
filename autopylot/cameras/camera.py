"""Wrapper for cameras."""
from ..utils import memory, settings


def Camera(
    memory=memory.mem,
    camera_type=settings.settings.CAMERA_TYPE,
    shape=tuple(settings.settings.IMAGE_SHAPE),
    *args,
    **kwargs,
):
    """Init Camera class.

    Args:
        camera_type (str, optional): Camera type. Defaults to "webcam".
        shape (tuple, optional): output shape of the captured image. Defaults to (160, 120, 3).

    Raises:
        ValueError: raise a valueError if camera_type is not supported.
    """
    if camera_type == "dummy":
        from .dummy import Dummy

        return Dummy(memory=memory, shape=shape, *args, **kwargs)
    elif camera_type == "replay":
        from .replay import Replay

        return Replay(memory=memory, shape=shape, *args, **kwargs)
    elif camera_type == "webcam":
        from .webcam import Webcam

        return Webcam(memory=memory, shape=shape, *args, **kwargs)
    elif camera_type == "sim":
        from .sim_webcam import SimWebcam

        return SimWebcam(memory=memory, shape=shape, *args, **kwargs)
    else:
        raise ValueError(f"Unknown camera type {camera_type}")
