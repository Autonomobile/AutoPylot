"""Memory class that we will be using throughout the project."""
import logging
import time


class Memory(dict):
    """Memory class, inherits from dict."""

    def __init__(self):
        """Init of the memory class."""
        self.last_modified = 0
        logging.info("Memory class initialized.")

    def __setitem__(self, key, value):
        """Set a key to a value.

        Args:
            key (string or integer): key.
            value (any): value.
        """
        self.last_modified = time.time()
        super().__setitem__(key, value)

    def __add__(self, other):
        """Addition of two dict.

        Args:
            other (dict): dict to add to.
        """
        if isinstance(other, dict):
            super().update(other)
        else:
            raise TypeError("other must be a dict")


mem = Memory()
