import numpy as np


class PrepareData:
    """Class to prepare data from the memory according to the needed model inputs."""

    def __init__(self, model_info):
        """init of the class

        Args:
            model_info (dict): the inputs / outputs info of the model.
        """
        self.inputs = model_info["inputs"]

    def __call__(self, mem):
        """Prepare the data.

        Args:
            mem (dict): the memory.

        Returns:
            list(np.array): the input data ready to be fed to the model.
        """
        input_data = []
        for name, _ in self.inputs:
            input_data.append(np.expand_dims(mem[name], 0).astype(np.float32))
        return input_data
