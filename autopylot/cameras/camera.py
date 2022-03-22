"""Wrapper for cameras."""
from ..utils import memory, settings
from .dummy import Dummy
from .replay import Replay
from .webcam import Webcam
from .sim_webcam import SimWebcam


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
    if camera_type == "webcam":
        return Webcam(memory=memory, shape=shape, *args, **kwargs)
    elif camera_type == "dummy":
        return Dummy(memory=memory, shape=shape, *args, **kwargs)
    elif camera_type == "replay":
        return Replay(memory=memory, shape=shape, *args, **kwargs)
    elif camera_type == "sim":
        return SimWebcam(memory=memory, shape=shape, *args, **kwargs)
    else:
        raise ValueError(f"Unknown camera type {camera_type}")
