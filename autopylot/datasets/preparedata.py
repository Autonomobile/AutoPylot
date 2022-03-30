"""Class to prepare the data before prediction."""
import numpy as np


class PrepareData:
    """Class to prepare data from the memory according to the needed model inputs."""

    def __init__(self, model_info):
        """Init of the class.

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
            try:
                data = np.expand_dims(mem[name], 0).astype(np.float32)
                if len(data.shape) < 2:
                    data = np.expand_dims(data, 0)
                input_data.append(data)
            except KeyError:
                raise ValueError(f"input name {name} is not in memory")
        return input_data
