"""Dummy camera for testing purposes."""
import logging

import numpy as np

from ..utils import memory, settings


class Dummy:
    """Dummy camera."""

    def __init__(
        self,
        memory=memory.mem,
        shape=tuple(settings.settings.image_shape),
    ):
        """Camera init.

        Args:
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """
        self.memory = memory

        self.shape = shape
        assert len(self.shape) == 3, "Shape should have 3 dimensions"
        self.h, self.w, self.c = self.shape
        assert self.c in [
            1,
            3,
        ], "Image last dimension should be either 3 (RGB) or 1 (GREY)"
        logging.info("Instantiated Dummy camera.")

    def update(self):
        """Create a dummy image."""
        self.memory["image"] = np.zeros(self.shape, dtype=np.float32)
