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
        indexes,
        paths,
        inp_out,
        batch_size=64,
        additionnal_funcs=[],
    ):
        """Init of the class.

        Args:
            indexes (list): list of indexes of the paths to use.
            paths (list): list or list of list of json_paths to train on.
            inp_out (dict): parsed input and output dict.
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

        assert len(indexes) != 0, "indexes should be non-empty"
        self.indexes = indexes
        self.paths = paths

        if self.dimensions == 0:
            self.lenpaths = len(paths)
        else:
            self.lenpaths = 0
            for seq in paths:
                self.lenpaths += len(seq)

        assert len(inp_out.keys()) != 0, "inp_out keys should be non-empty"
        self.inp_out = inp_out

        self.transformer = transform.Transform(additionnal_funcs)

    def __data_generation(self):
        """Prepare a batch of data for training.

        X represents the input data, and Y the expected outputs (as in Y=f(X))
        both are list of numpy arrays containing the data.
        For example, if we have N data and inputs = ["image", "speed"]
        X[0].shape = (N, 120, 160, 3) | we have N images of shape (120, 160, 3).
        X[1].shape = (N, 1) | we have N speed scalar.
        if we have outputs = ["steering", "throttle"]
        Y[0].shape = (N, 1) | we have N steering scalar.
        Y[1].shape = (N, 1) | we have N throttle scalar.

        Returns:
            tuple(list, list): X and Y.
        """
        X = {}
        Y = {}
        for idx in self.inp_out.keys():
            for inp, layer_name in self.inp_out[idx]["inputs"]:
                X[layer_name] = []
            for out, layer_name in self.inp_out[idx]["outputs"]:
                Y[layer_name] = []

        rand = np.random.uniform(0.0, 1.0)
        rdm_indexes = np.random.randint(0, len(self.indexes), self.batch_size)

        for rdm_idx in rdm_indexes:
            (i, j) = self.indexes[rdm_idx]
            rands = None

            for idx in self.inp_out.keys():
                json_path = self.paths[i][j + idx]
                if "image" in [
                    k[0] for k in self.inp_out[idx]["inputs"]
                ] or "image" in [k[0] for k in self.inp_out[idx]["inputs"]]:
                    image_data = io.load_image_data(json_path)
                else:
                    image_data = io.load_json(json_path)

                image_data["batch-random"] = rand
                rands = self.transformer(image_data, rands)

                for (inp, layer_name) in self.inp_out[idx]["inputs"]:
                    data = np.asarray(image_data[inp])
                    X[layer_name].append(data)

                for (out, layer_name) in self.inp_out[idx]["outputs"]:
                    data = np.asarray(image_data[out])
                    Y[layer_name].append(data)

        for k in X.keys():
            X[k] = np.array(X[k])
        for k in Y.keys():
            Y[k] = np.array(Y[k])

        return X, Y

    def __len__(self):
        return self.lenpaths

    def __getitem__(self, index):
        return self.__data_generation()
