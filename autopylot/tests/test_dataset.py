"""test the File.IO class"""

import glob
import os
import shutil
import sys

import numpy as np
import pytest

from ..datasets import dataset
from ..utils import io, settings

settings = settings.settings

dataset_path = os.path.join(settings.DATASET_PATH, "test_dataset")
dataset_one = os.path.join(dataset_path, "1")
dataset_two = os.path.join(dataset_path, "2")


def __convert_path(path):
    """Util function to convert path according to the current os.

    Args:
        path (str): the path.

    Returns:
        str: the converted path.
    """
    if sys.platform == "win32":
        return path.replace("/", "\\")
    else:
        return path.replace("\\", "/")


def test_sort_paths_is_sorted():
    """Testing if sort_paths() returns sorted elements."""
    paths = [
        __convert_path("mypath\\test\\1000.json"),
        __convert_path("hello/1.2.json"),
        __convert_path("yo/hella/weird/666.json"),
    ]
    correct = [
        __convert_path("hello/1.2.json"),
        __convert_path("yo/hella/weird/666.json"),
        __convert_path("mypath\\test\\1000.json"),
    ]
    assert correct == dataset.sort_paths(paths)


def test___get_time_stamp():
    """Testing if the function __get_time_stamp() works."""
    float_val = dataset.__get_time_stamp(__convert_path("mypath\\test\\35438.455.json"))
    assert isinstance(float_val, float)


def test_create_directory():
    """Create a testing_io directory."""
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    assert os.path.isdir(dataset_path)


def test_load_dataset_empty():
    """Test if the function load_dataset works."""
    list_of_dict = dataset.load_dataset(dataset_path)
    assert list_of_dict == []


def test_load_multiple_dataset_empty():
    """Testing if the function load_multiple_dataset() works."""
    ret_false = dataset.load_multiple_dataset(dataset_path, False)
    ret_true = dataset.load_multiple_dataset(dataset_path, True)
    assert ret_false == [] and ret_true == []


def test_save_dataset():
    """Fill the dataset directory with some data."""
    image_datas = [
        {
            "image": np.zeros((160, 120, 3), dtype=np.uint8),
            "steering": 0.33,
            "throttle": 0.5,
        },
        {
            "image": np.zeros((160, 120, 3), dtype=np.uint8),
            "steering": -0.6,
            "throttle": 0.7,
        },
    ]

    ret = io.save_image_data(image_datas[0], dataset_path + os.sep + "2.json")
    assert ret == (True, True)

    ret = io.save_image_data(image_datas[1], dataset_path + os.sep + "11.json")
    assert ret == (True, True)


def test_number_files():
    """Check the number of files in the directory."""
    # In total, there should be 2 * 2 = 4 files
    filepaths = glob.glob(dataset_path + os.sep + "*")
    assert len(filepaths) == 4

    # 2 .json
    jsonpaths = glob.glob(dataset_path + os.sep + "*.json")
    assert len(jsonpaths) == 2

    # 2 .png
    imagepaths = glob.glob(dataset_path + os.sep + "*.png")
    assert len(imagepaths) == 2


@pytest.mark.win
def test_load_dataset():
    """Testing if the function load_dataset() works."""
    datas = dataset.load_dataset(dataset_path)
    assert len(datas) == 2
    assert datas[0]["steering"] == -0.6 and datas[0]["throttle"] == 0.7
    assert datas[1]["steering"] == 0.33 and datas[1]["throttle"] == 0.5


@pytest.mark.win
def test_load_dataset_generator():
    """Testing if the function load_dataset_generator() works."""
    generator = dataset.load_dataset_generator(dataset_path)

    data = next(generator)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7

    data = next(generator)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5


def test_load_sorted_dataset():
    """Testing if the function load_sorted_dataset() works."""
    datas = dataset.load_sorted_dataset(dataset_path)
    assert len(datas) == 2
    assert datas[0]["steering"] == 0.33 and datas[0]["throttle"] == 0.5
    assert datas[1]["steering"] == -0.6 and datas[1]["throttle"] == 0.7


def test_delete_directory():
    """Deletes the created directory."""
    shutil.rmtree(dataset_path)
    assert os.path.exists(dataset_path) is False


def test_create_multiple_directories():
    """Create a testing_io directory containing two other directories.

    Returns:
        string : path to testing_io directory.
    """
    os.mkdir(dataset_path)
    assert os.path.isdir(dataset_path)

    os.mkdir(dataset_one)
    assert os.path.isdir(dataset_one)

    os.mkdir(dataset_two)
    assert os.path.isdir(dataset_two)


def test_save_multiple_dataset():
    """Fill the dataset directory with some data."""
    image_datas = [
        {
            "image": np.zeros((160, 120, 3), dtype=np.uint8),
            "steering": 0.33,
            "throttle": 0.5,
        },
        {
            "image": np.zeros((160, 120, 3), dtype=np.uint8),
            "steering": -0.6,
            "throttle": 0.7,
        },
        {
            "image": np.zeros((160, 120, 3), dtype=np.uint8),
            "steering": 0.1,
            "throttle": 0.1,
        },
    ]

    ret = io.save_image_data(image_datas[0], dataset_one + os.sep + "2.json")
    assert ret == (True, True)

    ret = io.save_image_data(image_datas[1], dataset_one + os.sep + "11.json")
    assert ret == (True, True)

    ret = io.save_image_data(image_datas[2], dataset_two + os.sep + "1.2.json")
    assert ret == (True, True)


@pytest.mark.win
def test_load_multiple_dataset_not_flat():
    """Testing if the function load_multiple_dataset() not flat works."""
    list_datas = dataset.load_multiple_dataset(dataset_path)

    datas = list_datas[0]
    assert len(datas) == 2
    assert datas[0]["steering"] == -0.6 and datas[0]["throttle"] == 0.7
    assert datas[1]["steering"] == 0.33 and datas[1]["throttle"] == 0.5

    datas = list_datas[1]
    assert len(datas) == 1
    assert datas[0]["steering"] == 0.1 and datas[0]["throttle"] == 0.1


@pytest.mark.win
def test_load_multiple_dataset_flat():
    """Testing if the function load_multiple_dataset() flat works."""
    datas = dataset.load_multiple_dataset(dataset_path, True)

    assert len(datas) == 3
    assert datas[0]["steering"] == -0.6 and datas[0]["throttle"] == 0.7
    assert datas[1]["steering"] == 0.33 and datas[1]["throttle"] == 0.5
    assert datas[2]["steering"] == 0.1 and datas[2]["throttle"] == 0.1


@pytest.mark.win
def test_load_multiple_sorted_dataset_not_flat():
    """Testing if the function load_multiple_sorted_dataset() not flat works."""
    list_datas = dataset.load_multiple_sorted_dataset(dataset_path)

    datas = list_datas[0]
    assert len(datas) == 2
    assert datas[0]["steering"] == 0.33 and datas[0]["throttle"] == 0.5
    assert datas[1]["steering"] == -0.6 and datas[1]["throttle"] == 0.7

    datas = list_datas[1]
    assert len(datas) == 1
    assert datas[0]["steering"] == 0.1 and datas[0]["throttle"] == 0.1


@pytest.mark.win
def test_load_multiple_dataset_generator_not_flat():
    """Testing if the function load_multiple_dataset_generator() not flat works."""
    generator = dataset.load_multiple_dataset_generator(dataset_path)

    gen = next(generator)
    data = next(gen)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7
    data = next(gen)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5

    gen = next(generator)
    data = next(gen)
    assert data["steering"] == 0.1 and data["throttle"] == 0.1


@pytest.mark.win
def test_load_multiple_dataset_generator_flat():
    """Testing if the function load_multiple_dataset_generator() flat works."""
    generator = dataset.load_multiple_dataset_generator(dataset_path, True)

    data = next(generator)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7
    data = next(generator)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5
    data = next(generator)
    assert data["steering"] == 0.1 and data["throttle"] == 0.1


@pytest.mark.win
def test_load_multiple_sorted_dataset_generator_flat():
    """Testing if the function load_multiple_sorted_dataset_generator() flat works."""
    generator = dataset.load_multiple_sorted_dataset_generator(dataset_path, True)

    data = next(generator)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5
    data = next(generator)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7
    data = next(generator)
    assert data["steering"] == 0.1 and data["throttle"] == 0.1


def test_delete_multiple_directories():
    """Deletes the created directory."""
    shutil.rmtree(dataset_path)
    assert os.path.exists(dataset_path) is False
