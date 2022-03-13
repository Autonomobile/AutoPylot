"""Wrapper for cameras."""
from ..utils import memory
from .dummy import Dummy
from .replay import Replay
from .webcam import Webcam


def Camera(
    memory=memory.mem,
    camera_type="webcam",
    shape=(120, 160, 3),
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
        return Webcam(memory, *args, **kwargs, shape=shape)
    elif camera_type == "dummy":
        return Dummy(memory, *args, **kwargs, shape=shape)
    elif camera_type == "replay":
        return Replay(memory, *args, **kwargs, shape=shape)
    else:
        raise ValueError("Unknown camera type")
