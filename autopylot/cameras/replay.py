"""Replay camera."""
import logging

import cv2

from ..datasets import dataset


class Replay:
    """Replay camera class."""

    def __init__(self, memory, dataset_path, shape=(120, 160, 3)):
        """Camera init.

        Args:
            dataset_path (string): path to the dataset to load.
            shape (tuple, optional): shape of the output image. Defaults to (160, 120, 3).
        """
        self.memory = memory
        self.dataset_path = dataset_path

        self.generator = self.create_generator()

        # Check that we have at least one data in our dataset
        try:
            next(self.generator)
        except StopIteration:
            raise ValueError("Please provide a valid dataset path.")

        self.shape = shape
        assert len(self.shape) == 3, "Shape should have 3 dimensions"

        self.h, self.w, self.c = self.shape
        assert self.c in [
            1,
            3,
        ], "Image last dimension should be either 3 (RGB) or 1 (GREY)"
        logging.info("Instantiated Replay camera.")

    def update(self):
        """Read image by fetching the next element from the generator."""

        img = self.fetch_image()
        img = cv2.resize(img, (self.w, self.h))
        if self.c == 3:
            self.memory["image"] = img
        else:
            self.memory["image"] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def create_generator(self):
        return dataset.load_sorted_dataset_generator(self.dataset_path)

    def fetch_image(self):
        try:
            data = next(self.generator)
        except StopIteration:
            # re-create a generator (loop the dataset)
            self.generator = self.create_generator()
        return data["image"]
