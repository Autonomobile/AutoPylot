"""test the File.IO class"""

import glob
import os
import shutil
import sys

import numpy as np
import pytest

from ..datasets import dataset
from ..utils import io

path_dir = os.path.join(os.getcwd(), "testing_dataset")
dir_one = os.path.join(path_dir, "1")
dir_two = os.path.join(path_dir, "2")


def __convert_path(path):
    """Util function to convert path according to the current os

    Args:
        path (str): the path.

    Returns:
        str: the converted path.
    """
    if sys.platform == "win32":
        return path.replace("/", "\\")
    else:
        return path.replace("\\", "/")


def test___sort_paths_is_sorted():
    """Testing if __sort_paths() returns sorted elements."""
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
    assert correct == dataset.__sort_paths(paths)


def test___get_time_stamp():
    """Testing if the function __get_time_stamp() works"""
    float_val = dataset.__get_time_stamp(__convert_path("mypath\\test\\35438.455.json"))
    assert isinstance(float_val, float)


def test_create_directory():
    """Create a testing_io directory.
    Returns:
        string : path to testing_io directory.
    """
    os.mkdir(path_dir)
    assert os.path.isdir(path_dir)


def test_load_dataset_empty():
    """test if the function load_dataset works."""
    list_of_dict = dataset.load_dataset(path_dir)
    assert list_of_dict == []


def test_load_multiple_dataset_empty():
    """Testing if the function load_multiple_dataset() works"""
    ret_false = dataset.load_multiple_dataset(path_dir, False)
    ret_true = dataset.load_multiple_dataset(path_dir, True)
    assert ret_false == [] and ret_true == []


def test_save_dataset():
    """Fill the dataset directory with some data."""
    image_datas = [
        {
            "image": np.zeros((160, 120, 3), dtype=np.float32),
            "steering": 0.33,
            "throttle": 0.5,
        },
        {
            "image": np.zeros((160, 120, 3), dtype=np.float32),
            "steering": -0.6,
            "throttle": 0.7,
        },
    ]

    ret = io.save_image_data(image_datas[0], path_dir + os.sep + "2.json")
    assert ret == (True, True)

    ret = io.save_image_data(image_datas[1], path_dir + os.sep + "11.json")
    assert ret == (True, True)


def test_number_files():
    """Check the number of files in the directory."""

    # In total, there should be 2 * 2 = 4 files
    filepaths = glob.glob(path_dir + os.sep + "*")
    assert len(filepaths) == 4

    # 2 .json
    jsonpaths = glob.glob(path_dir + os.sep + "*.json")
    assert len(jsonpaths) == 2

    # 2 .png
    imagepaths = glob.glob(path_dir + os.sep + "*.png")
    assert len(imagepaths) == 2


@pytest.mark.win
def test_load_dataset():
    """Testing if the function load_dataset() works."""
    datas = dataset.load_dataset(path_dir)
    assert len(datas) == 2
    assert datas[0]["steering"] == -0.6 and datas[0]["throttle"] == 0.7
    assert datas[1]["steering"] == 0.33 and datas[1]["throttle"] == 0.5


@pytest.mark.win
def test_load_dataset_generator():
    """Testing if the function load_dataset_generator() works."""
    generator = dataset.load_dataset_generator(path_dir)

    data = next(generator)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7

    data = next(generator)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5


def test_load_sorted_dataset():
    """Testing if the function load_sorted_dataset() works."""
    datas = dataset.load_sorted_dataset(path_dir)
    assert len(datas) == 2
    assert datas[0]["steering"] == 0.33 and datas[0]["throttle"] == 0.5
    assert datas[1]["steering"] == -0.6 and datas[1]["throttle"] == 0.7


def test_delete_directory():
    """Deletes the created directory."""
    shutil.rmtree(path_dir)
    assert os.path.exists(path_dir) is False


def test_create_multiple_directories():
    """Create a testing_io directory containing two other directories.
    Returns:
        string : path to testing_io directory.
    """
    os.mkdir(path_dir)
    assert os.path.isdir(path_dir)

    os.mkdir(dir_one)
    assert os.path.isdir(dir_one)

    os.mkdir(dir_two)
    assert os.path.isdir(dir_two)


def test_save_multiple_dataset():
    """Fill the dataset directory with some data."""
    image_datas = [
        {
            "image": np.zeros((160, 120, 3), dtype=np.float32),
            "steering": 0.33,
            "throttle": 0.5,
        },
        {
            "image": np.zeros((160, 120, 3), dtype=np.float32),
            "steering": -0.6,
            "throttle": 0.7,
        },
        {
            "image": np.zeros((160, 120, 3), dtype=np.float32),
            "steering": 0.1,
            "throttle": 0.1,
        },
    ]

    ret = io.save_image_data(image_datas[0], dir_one + os.sep + "2.json")
    assert ret == (True, True)

    ret = io.save_image_data(image_datas[1], dir_one + os.sep + "11.json")
    assert ret == (True, True)

    ret = io.save_image_data(image_datas[2], dir_two + os.sep + "1.2.json")
    assert ret == (True, True)


@pytest.mark.win
def test_load_multiple_dataset_not_flat():
    """Testing if the function load_multiple_dataset() not flat works."""
    list_datas = dataset.load_multiple_dataset(path_dir)

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
    datas = dataset.load_multiple_dataset(path_dir, True)

    assert len(datas) == 3
    assert datas[0]["steering"] == -0.6 and datas[0]["throttle"] == 0.7
    assert datas[1]["steering"] == 0.33 and datas[1]["throttle"] == 0.5
    assert datas[2]["steering"] == 0.1 and datas[2]["throttle"] == 0.1


def test_load_multiple_sorted_dataset():
    """Testing if the function load_multiple_sorted_dataset() works."""
    list_datas = dataset.load_multiple_sorted_dataset(path_dir)

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
    generator = dataset.load_multiple_dataset_generator(path_dir)

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
    generator = dataset.load_multiple_dataset_generator(path_dir, True)

    data = next(generator)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7
    data = next(generator)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5
    data = next(generator)
    assert data["steering"] == 0.1 and data["throttle"] == 0.1


def test_load_multiple_sorted_dataset_generator_flat():
    """Testing if the function load_multiple_sorted_dataset_generator() flat works."""
    generator = dataset.load_multiple_sorted_dataset_generator(path_dir, True)

    data = next(generator)
    assert data["steering"] == 0.33 and data["throttle"] == 0.5
    data = next(generator)
    assert data["steering"] == -0.6 and data["throttle"] == 0.7
    data = next(generator)
    assert data["steering"] == 0.1 and data["throttle"] == 0.1


def test_delete_multiple_directories():
    """Deletes the created directory."""
    shutil.rmtree(path_dir)
    assert os.path.exists(path_dir) is False
