import cv2


def identity_transform(memory, image_key):
    """Simple function to return the image at "image_key" in the memory.

    Args:
        memory (dictionnary): memory dict.
        image_key (string): image key.

    Returns:
        np.array: the image.
    """
    return memory[image_key]


class Display:
    """Display class to display images."""

    def __init__(
        self,
        memory,
        window_names=["image"],
        image_keys=["image"],
        transform_funcs=[identity_transform],
        waitKey=1,
    ):
        self.memory = memory
        self.window_names = window_names
        self.image_keys = image_keys
        self.transform_funcs = transform_funcs
        self.waitKey = waitKey

        # check if the number of items in every lists is the same.
        assert len(window_names) == len(image_keys) == len(transform_funcs)

    def update(self):
        """Display every item in image_keys list using transform_funcs."""

        for win_name, image_key, func in zip(
            self.window_names, self.image_keys, self.transform_funcs
        ):
            cv2.imshow(win_name, func(self.memory, image_key))

        cv2.waitKey(self.waitKey)
