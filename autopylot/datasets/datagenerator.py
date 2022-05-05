"""
Class to load data on the go to train the model.
This class inherits from Sequence, a tensorflow.keras utils.
"""
import logging

import numpy as np
from tensorflow.keras.utils import Sequence

from ..utils import io
from . import transform


class DataGenerator(Sequence):
    def __init__(
        self,
        paths,
        inputs=["image"],
        outputs=["steering"],
        batch_size=64,
        additionnal_funcs=[],
    ):
        """Init of the class.

        Args:
            paths (list): list or list of list of json_paths to train on.
            inputs (list, optional): _description_. Defaults to ["image"].
            outputs (list, optional): _description_. Defaults to ["steering"].
            batch_size (int, optional): _description_. Defaults to 64.
            additionnal_funcs (list(tuple(method, float)), optional): tuple containing the function and the frequency.

        Raises:
            ValueError: paths should be non-empty
        """

        # determine whether we were given a list or a list of list
        self.batch_size = batch_size
        assert len(paths) != 0, "paths should be non-empty"
        if isinstance(paths[0], str):
            self.dimensions = 0
        elif isinstance(paths[0][0], str):
            self.dimensions = 1
        else:
            raise ValueError("Unknown type")
        self.paths = paths
        self.lenpaths = len(paths)

        assert len(inputs) != 0, "there should be at least one input"
        self.inputs = inputs

        assert len(outputs) != 0, "there should be at least one output"
        self.outputs = outputs

        self.transformer = transform.Transform(additionnal_funcs)

    def __data_generation(self):
        """Prepare a batch of data for training.

        X represents the input data, and Y the expected outputs (as in Y=f(X))
        both are list of numpy arrays containing the data.
        For example, if we have N data and inputs = ["image", "speed"]
        X[0].shape = (N, 120, 160, 3) | we have N images of shape (120, 160, 3).
        X[1].shape = (N, 1) | we have N speed scalar.
        if we have outputs = [""steering", "throttle"]
        Y[0].shape = (N, 1) | we have N steering scalar.
        Y[1].shape = (N, 1) | we have N throttle scalar.

        Returns:
            tuple(list, list): X and Y.
        """
        X = [[] for _ in range(len(self.inputs))]
        Y = [[] for _ in range(len(self.outputs))]

        rdm_paths = np.random.choice(self.paths, size=self.batch_size)
        for path in rdm_paths:
            try:
                image_data = io.load_image_data(path)
                self.transformer(image_data)
                for i, inp in enumerate(self.inputs):
                    data = np.array(image_data[inp])
                    X[i].append(data)

                for i, out in enumerate(self.outputs):
                    data = np.array(image_data[out])
                    Y[i].append(data)
            except Exception:
                logging.debug(f"Error processing {path}")

        X = [np.array(x) for x in X]
        Y = [np.array(y) for y in Y]

        return X, Y

    def __len__(self):
        return self.lenpaths

    def __getitem__(self, index):
        return self.__data_generation()
