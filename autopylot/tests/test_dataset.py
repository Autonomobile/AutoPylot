"""test the File.IO class"""
import os
import time
import glob

import numpy as np

from ..datasets import dataset
from ..utils import io


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


# TODO: Test the loading of the data


def test_delete_directory():
    """Deletes the created directory."""
    path_dir = os.path.join(os.getcwd(), "testing_dataset")
    files_to_delete = glob.glob(path_dir + "\\*")

    for filepath in files_to_delete:
        os.remove(filepath)

    os.rmdir(path_dir)
    assert os.path.exists(path_dir) is False
