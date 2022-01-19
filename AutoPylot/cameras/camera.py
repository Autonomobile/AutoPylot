"""Wrapper for cameras."""
from .webcam import Webcam
from .dummy import Dummy


def Camera(camera_type="webcam", shape=(160, 120, 3), *args, **kwargs):
    """Init Camera class.

    Args:
        camera_type (str, optional): [description]. Defaults to "webcam".
        shape (tuple, optional): [description]. Defaults to (160, 120, 3).

    Raises:
        ValueError: raise a valueError if camera_type is not supported.
    """
    if camera_type == "webcam":
        return Webcam(*args, **kwargs, shape=shape)
    elif camera_type == "dummy":
        return Dummy(*args, **kwargs, shape=shape)
    else:
        raise ValueError("Unknown camera type")
