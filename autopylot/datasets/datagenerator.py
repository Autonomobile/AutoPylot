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

        X = []
        Y = []
        loaded_img = []
        loaded_speed = []
        loaded_throttle = []
        loaded_steering = []
        for i in range(64):
            path = random.choice(self.paths)
            data = np.array(list(io.load_image_data(path).items()))
            if data[0][0] == "image" : #case where input == image 
                loaded_img.append(data[0][1])
            if data[1][0] == "speed" : #case where input == speed 
                loaded_speed.append([data[1][1]])
        X.append(np.array(loaded_img))
        X.append(np.array(loaded_speed))

        for j in range(64):
            path = random.choice(self.paths)
            data = np.array(list(io.load_image_data(path).items())) #data= list of list of items 
            if data[2][0] == "throttle" : #case where input == steering 
                loaded_steering.append([data[2][1]])
            if data[3][0] == "steering" : #case where input == throttle 
                loaded_throttle.append([data[3][1]])
        Y.append(np.array(loaded_steering))
        Y.append(np.array(loaded_throttle))       

        return X, Y

    def __len__(self):
        return self.lenpaths

    def __getitem__(self, index):
        return self.__data_generation()
