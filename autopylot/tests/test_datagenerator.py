"""Test the DataGenerator class."""
import os

import numpy as np

from ..datasets import datagenerator
from ..utils import io


def test_save_data():
    """Just create a dummy data for the following functions."""
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "speed": 1.4,
        "throttle": 0.6,
        "steering": 0.04,
    }
    io.save_image_data(image_data, "dummy_path.json")
    assert os.path.exists("dummy_path.json")


def test_init():
    """Test the init of the DataGenerator class."""
    dataGenerator = datagenerator.DataGenerator(
        ["dummy_path.json"],
        inputs=["image", "speed"],
        outputs=["steering", "throttle"],
        batch_size=64,
    )
    assert dataGenerator.dimensions == 0
    assert dataGenerator.batch_size == 64
    assert dataGenerator.inputs == ["image", "speed"]
    assert dataGenerator.outputs == ["steering", "throttle"]
    assert len(dataGenerator) == len(dataGenerator.paths)


def test_call():
    """Test the call of the DataGenerator class."""

    dataGenerator = datagenerator.DataGenerator(
        ["dummy_path.json"],
        inputs=["image", "speed"],
        outputs=["steering", "throttle"],
        batch_size=64,
    )
    Xs, Ys = dataGenerator[0]  # calls the __getitem__ method
    assert isinstance(Xs, list) and isinstance(Ys, list)

    assert Xs[0].shape == (64, 120, 160, 3)  # the image input
    assert Xs[1].shape == (64, 1, 1)  # the speed input

    assert Ys[0].shape == (64, 1, 1)  # the steering output
    assert Ys[1].shape == (64, 1, 1)  # the throttle output


def test_delete_data():
    """Delete the previously created image and json."""
    os.remove("dummy_path.json")
    os.remove("dummy_path.png")
    assert not os.path.exists("dummy_path.json") and not os.path.exists(
        "dummy_path.png"
    )
