"""Webcam camera."""
import logging

import cv2

from ..utils import memory, settings


class Webcam:
    """Webcam class."""

    def __init__(
        self,
        memory=memory.mem,
        index=0,
        shape=tuple(settings.settings.image_shape),
    ):
        """Camera init.

        Args:
            index (int, optional): index of the camera. Defaults to 0.
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """
        self.memory = memory

        self.cap = cv2.VideoCapture(index)
        ret, img = self.cap.read()
        assert ret, "Couldn't read from camera"

        self.shape = shape
        assert len(self.shape) == 3, "Shape should have 3 dimensions"

        self.h, self.w, self.c = self.shape
        assert self.c in [
            1,
            3,
        ], "Image last dimension should be either 3 (RGB) or 1 (GREY)"
        logging.info("Instantiated Webcam camera.")

    def update(self):
        """Read image from the camera.

        Raises:
            ValueError: if couldn't grab the image, raise a valueError.
        """
        ret, img = self.cap.read()
        if ret:
            img = cv2.resize(img, (self.w, self.h))
            if self.c == 3:
                self.memory["image"] = img
            else:
                self.memory["image"] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        else:
            raise ValueError("Image read failed")
