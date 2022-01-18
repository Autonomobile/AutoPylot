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
        self.h = shape[0]
        self.w = shape[1]
        assert len(self.shape) == 3, "Shape should have 3 dimensions"
        assert self.shape[-1] == 3 or self.shape[-1] == 1, "Image last dimension should be either 3 (RGB) or 1 (GREY)"

    def _resize(self, img):
        """Resize the image to the given shape of output image.

        Args:
            img (np.array): image

        Returns:
            np.array: resized image
        """
        return cv2.resize(img, (self.w, self.h))

    def read(self):
        """Read image from the camera.

        Raises:
            ValueError: if couldn't grab the image, raise a valueError.

        Returns:
            np.array: resized image
        """
        ret, img = self.cap.read()
        if ret:
            return self.resize(img)
        else:
            raise ValueError("Image read failed")
