"""Test the DataGenerator class."""
import os

import numpy as np

from ..datasets import datagenerator
from ..utils import io


def test_save_data():
    """Just create a dummy data for the following functions."""
    image_data = {
        "image": np.zeros((120, 160, 3), np.uint8),
        "speed": 1.4,
        "throttle": 0.6,
        "steering": 0.04,
    }
    io.save_image_data(image_data, "dummy_path.json")
    assert os.path.exists("dummy_path.json")


def test_init():
    """Test the init of the DataGenerator class."""
    inp_out = {
        0: {
            "inputs": ["image", "speed"],
            "outputs": ["steering", "throttle"],
        }
    }

    dataGenerator = datagenerator.DataGenerator(
        [(0, 0)],
        [["dummy_path.json"]],
        inp_out,
        batch_size=64,
    )
    assert dataGenerator.batch_size == 64
    assert len(dataGenerator) == len(dataGenerator.paths)


def test_call():
    """Test the call of the DataGenerator class."""

    inp_out = {
        0: {
            "inputs": [("image", "image"), ("speed", "speed")],
            "outputs": [("steering", "steering"), ("throttle", "throttle")],
        }
    }

    dataGenerator = datagenerator.DataGenerator(
        [(0, 0)],
        [["dummy_path.json"]],
        inp_out,
        batch_size=64,
    )

    Xs, Ys = dataGenerator[0]  # calls the __getitem__ method
    assert isinstance(Xs, dict) and isinstance(Ys, dict)

    assert Xs["image"].shape == (64, 120, 160, 3)  # the image input
    assert Xs["speed"].shape == (64,)  # the speed input

    assert Ys["steering"].shape == (64,)  # the steering output
    assert Ys["throttle"].shape == (64,)  # the throttle output


def test_call_no_image():
    """Test the call of the DataGenerator class when no image is present."""

    inp_out = {
        0: {
            "inputs": [("speed", "speed"), ("throttle", "throttle")],
            "outputs": [("steering", "steering"), ("throttle", "throttle")],
        }
    }

    dataGenerator = datagenerator.DataGenerator(
        [(0, 0)],
        [["dummy_path.json"]],
        inp_out,
        batch_size=32,
    )
    Xs, Ys = dataGenerator[0]  # calls the __getitem__ method

    for inp in Xs.keys():
        assert Xs[inp].shape == (32,)

    for out in Ys.keys():
        assert Ys[out].shape == (32,)


def test_delete_data():
    """Delete the previously created image and json."""
    os.remove("dummy_path.json")
    os.remove("dummy_path.png")
    assert not os.path.exists("dummy_path.json") and not os.path.exists(
        "dummy_path.png"
    )
