"""
Class to load data on the go to train the model.
This class inherits from Sequence, a tensorflow.keras utils.
"""
import random
import numpy as np
from tensorflow.keras.utils import Sequence

from ..utils import io


class DataGenerator(Sequence):
    def __init__(self, paths, inputs=["image"], outputs=["steering"], batch_size=64):
        """Init of the class.

        Args:
            paths (list): list or list of list of json_paths to train on.
            inputs (list, optional): _description_. Defaults to ["image"].
            outputs (list, optional): _description_. Defaults to ["steering"].

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

    def __data_generation(self):
        # TODO
        # pick a given amount of paths,
        # load them using io.load_image_data
        # put those data the X / Y lists with the right
        # shape/dimension using inputs and outputs list of keys.

        # X represents the input data, and Y the expected outputs (as in Y=f(X))
        # both are list of numpy arrays containing the data.
        # For example, if we have N data and inputs = ["image", "speed"]
        # X[0].shape = (N, 120, 160, 3) | we have N images of shape (120, 160, 3).
        # X[1].shape = (N, 1) | we have N speed scalar.
        # if we have outputs = [""steering", "throttle"]
        # Y[0].shape = (N, 1) | we have N steering scalar.
        # Y[1].shape = (N, 1) | we have N throttle scalar.

        X = list()
        Y = list()
        # possible to add a while (n < self.paths_len) in order to load in advance and use Yield instead of return
        for input in self.inputs:
            L = list()
            try:
                for j in range(self.batch_size):
                    # pick a random path
                    path = random.choice(self.paths)
                    data = dict(io.load_image_data(path).items())
                    data = np.array(data[input])
                    if len(data.shape) < 2:
                        data = np.expand_dims(data, axis=0)
                    L.append(list(data))
                X.append(np.array(L))
            except Exception as e:
                pass

        for output in self.outputs:
            L = list()
            try:
                for j in range(self.batch_size):
                    data = np.array(output)
                    if len(data.shape) < 2:
                        data = np.expand_dims(data, axis=0)
                    L.append(list(data))
                Y.append(np.array(L))
            except Exception as e:
                pass
        return X, Y

    def __len__(self):
        return self.lenpaths

    def __getitem__(self, index):
        return self.__data_generation()
