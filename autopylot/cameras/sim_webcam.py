"""Sim webcam camera."""
import logging

import cv2

from ..utils import memory, settings, sim_client


class SimWebcam:
    """SimWebcam class."""

    def __init__(
        self,
        memory=memory.mem,
        shape=tuple(settings.settings.IMAGE_SHAPE),
        client=sim_client.client,
    ):
        """Camera init.

        Args:
            index (int, optional): index of the camera. Defaults to 0.
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """
        self.memory = memory

        assert client is not None, "please set CAMERA_TYPE to 'sim'"

        self.client = client
        assert self.client.image is not None

        self.shape = shape
        assert len(self.shape) == 3, "Shape should have 3 dimensions"

        self.h, self.w, self.c = self.shape
        assert self.c in [
            1,
            3,
        ], "Image last dimension should be either 3 (RGB) or 1 (GREY)"
        logging.info("Instantiated Sim Webcam camera.")

    def update(self):
        """Read image from the simulator client."""
        img = self.client.get_latest_image()
        img = cv2.resize(img, (self.w, self.h))
        if self.c == 3:
            self.memory["image"] = img
        else:
            self.memory["image"] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
