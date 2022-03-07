"""test the File.IO class"""

import glob
import os
import sys
import shutil
import time
import numpy as np
from ..datasets import dataset
from ..utils import io


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


def test_create_directory():
    """Create a testing_io directory.
    Returns:
        string : path to testing_io directory.
    """
    current_path = os.getcwd()
    new_path_dir = os.path.join(current_path, "testing_dataset")
    os.mkdir(new_path_dir)
    assert new_path_dir.endswith("testing_dataset")


def test_load_dataset_empty():
    """test if the function load_dataset works."""
    path_dir = os.path.join(os.getcwd(), "testing_dataset")
    list_of_dict = dataset.load_dataset(path_dir)
    assert list_of_dict == []


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

    for image_data in image_datas:
        tosave_path = os.path.join(
            os.getcwd(),
            "testing_dataset",
            str(time.time()) + ".json",
        )
        ret = io.save_image_data(image_data, tosave_path)
        assert ret == (True, True)


def test_number_files():
    """Check the number of files in the directory."""
    path_dir = os.path.join(os.getcwd(), "testing_dataset", "*")

    # In total, there should be 2 * 2 = 4 files
    filepaths = glob.glob(path_dir)
    assert len(filepaths) == 4

    # 2 .json
    jsonpaths = glob.glob(path_dir + ".json")
    assert len(jsonpaths) == 2

    # 2 .png
    imagepaths = glob.glob(path_dir + ".png")
    assert len(imagepaths) == 2


# Do to : make a test funtion for when flat is true then one for when flat is false.


def test_load_multiple_dataset_empty():
    """Testing if the function load_multiple_dataset() works"""
    path_dir = os.path.join(os.getcwd(), "testing_dataset") + os.sep
    ret_false = dataset.load_multiple_dataset(path_dir, False)
    ret_true = dataset.load_multiple_dataset(path_dir, True)
    assert ret_false == [] and ret_true == []


def test_load_dataset_generator():
    """Testing if the function load_dataset_generator() works."""
    path_dir = os.path.join(os.getcwd(), "testing_dataset") + os.sep
    list_of_dict = list(dataset.load_dataset_generator(path_dir))
    assert len(list_of_dict) == 2


def test___sort_paths_is_str():
    """Testing if __sort_paths() works."""
    path_dir = os.path.join(os.getcwd(), "testing_dataset")
    for path in glob.glob(path_dir + "*.json"):
        assert isinstance(path, str)


def test___sort_paths_is_sorted():
    """Testing if __sort_paths() returns sorted elements."""
    path_dir = [
        __convert_path("mypath\\test\\1000.json"),
        __convert_path("hello/1.2.json"),
        __convert_path("yo/hella/weird/666.json"),
    ]
    correct = [
        __convert_path("hello/1.2.json"),
        __convert_path("yo/hella/weird/666.json"),
        __convert_path("mypath\\test\\1000.json"),
    ]
    assert correct == dataset.__sort_paths(path_dir)


def test___get_time_stamp():
    """Testing if the function __get_time_stamp() works"""
    float_val = dataset.__get_time_stamp(__convert_path("mypath\\test\\35438.455.json"))
    assert isinstance(float_val, float)


def test_delete_directory():
    """Deletes the created directory."""
    path_dir = os.path.join(os.getcwd(), "testing_dataset")
    shutil.rmtree(path_dir)
    assert os.path.exists(path_dir) is False
