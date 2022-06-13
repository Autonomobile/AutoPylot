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

    index_map = {
        "inputs": {0: 0, 1: 1},
        "outputs": {0: 0, 1: 1},
    }

    dataGenerator = datagenerator.DataGenerator(
        [(0, 0)],
        [["dummy_path.json"]],
        inp_out,
        index_map,
        batch_size=64,
    )
    assert dataGenerator.batch_size == 64
    assert dataGenerator.num_inputs == 2
    assert dataGenerator.num_outputs == 2
    assert len(dataGenerator) == len(dataGenerator.paths)


def test_call():
    """Test the call of the DataGenerator class."""

    inp_out = {
        0: {
            "inputs": ["image", "speed"],
            "outputs": ["steering", "throttle"],
        }
    }

    index_map = {
        "inputs": {0: 0, 1: 1},
        "outputs": {0: 0, 1: 1},
    }

    dataGenerator = datagenerator.DataGenerator(
        [(0, 0)],
        [["dummy_path.json"]],
        inp_out,
        index_map,
        batch_size=64,
    )

    Xs, Ys = dataGenerator[0]  # calls the __getitem__ method
    assert isinstance(Xs, list) and isinstance(Ys, list)

    assert Xs[0].shape == (64, 120, 160, 3)  # the image input
    assert Xs[1].shape == (64,)  # the speed input

    assert Ys[0].shape == (64,)  # the steering output
    assert Ys[1].shape == (64,)  # the throttle output


def test_call_no_image():
    """Test the call of the DataGenerator class when no image is present."""

    inp_out = {
        0: {
            "inputs": ["speed", "throttle"],
            "outputs": ["steering", "throttle"],
        }
    }

    index_map = {
        "inputs": {0: 0, 1: 1},
        "outputs": {0: 0, 1: 1},
    }

    dataGenerator = datagenerator.DataGenerator(
        [(0, 0)],
        [["dummy_path.json"]],
        inp_out,
        index_map,
        batch_size=32,
    )
    Xs, Ys = dataGenerator[0]  # calls the __getitem__ method
    assert Xs[0].shape == (32,)  # the speed input
    assert Xs[1].shape == (32,)  # the throttle input

    assert Ys[0].shape == (32,)  # the steering output
    assert Ys[1].shape == (32,)  # the throttle output


def test_delete_data():
    """Delete the previously created image and json."""
    os.remove("dummy_path.json")
    os.remove("dummy_path.png")
    assert not os.path.exists("dummy_path.json") and not os.path.exists(
        "dummy_path.png"
    )
