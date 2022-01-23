"""Dummy camera for testing purposes."""
import numpy as np


class Dummy():
    """Dummy camera."""

    def __init__(self, memory, shape=(160, 120, 3)):
        """Camera init.

        Args:
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """
        self.memory = memory

        self.shape = shape
        self.h = shape[0]
        self.w = shape[1]
        self.c = shape[2]
        assert len(self.shape) == 3, "Shape should have 3 dimensions"
        assert self.c in [
            1, 3], "Image last dimension should be either 3 (RGB) or 1 (GREY)"

    def update(self):
        """Create a dummy image."""
        self.memory['image'] = np.zeros(self.shape, dtype=np.float32)
