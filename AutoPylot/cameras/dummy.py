
import numpy as np


class Dummy():
    """Dummy camera."""

    def __init__(self, shape=(160, 120, 3)):
        """Camera init.

        Args:
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """

        self.shape = shape
        assert self.shape[-1] == 3 or self.shape[-1] == 1, "Image last dimension should be either 3 (RGB) or 1 (GREY)"

    def read(self):
        """Create a dummy image.

        Returns:
            np.array: image
        """
        return np.zeros(self.shape, dtype=np.float32)
