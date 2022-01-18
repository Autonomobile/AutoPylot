"""Webcam camera."""
import cv2


class Webcam:
    """Webcam class."""

    def __init__(self, index=0, shape=(160, 120, 3)):
        """Camera init.

        Args:
            index (int, optional): index of the camera. Defaults to 0.
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """
        self.cap = cv2.VideoCapture(index)
        ret, img = self.cap.read()
        assert ret, "Couldn't read from camera"

        self.shape = shape
        assert len(self.shape) == 3, "Shape should have 3 dimensions"
        self.h = shape[0]
        self.w = shape[1]
        self.c = shape[2]
        assert self.c in [
            1, 3], "Image last dimension should be either 3 (RGB) or 1 (GREY)"

    def read(self):
        """Read image from the camera.

        Raises:
            ValueError: if couldn't grab the image, raise a valueError.

        Returns:
            np.array: resized image
        """
        ret, img = self.cap.read()
        if ret:
            img = cv2.resize(img, (self.w, self.h))
            return img if self.c == 3 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError("Image read failed")
