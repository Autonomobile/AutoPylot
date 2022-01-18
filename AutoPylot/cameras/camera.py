"""Wrapper for cameras."""
from .webcam import Webcam
from .dummy import Dummy


class Camera(Webcam, Dummy):
    """Camera class.

    Args:
        Webcam (class): Webcam camera
        Dummy (class): Dummy camera
    """

    def __init__(self, camera_type="webcam", shape=(160, 120, 3), *args, **kwargs):
        """Tnit class.

        Args:
            camera_type (str, optional): [description]. Defaults to "webcam".
            shape (tuple, optional): [description]. Defaults to (160, 120, 3).

        Raises:
            ValueError: raise a valueError if camera_type is not supported.
        """
        if camera_type == "webcam":
            Webcam.__init__(self, *args, **kwargs, shape=shape)
        elif camera_type == "dummy":
            Dummy.__init__(self, *args, **kwargs, shape=shape)
        else:
            raise ValueError("Unknown camera type")
