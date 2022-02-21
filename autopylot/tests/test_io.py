"""test the io class"""
import os
import shutil
import glob

import numpy as np
import pytest

from ..utils import io

"""
When on windows don't copy the path directly use one of the following ways: 
1.  use an r (raw) before the copied path (r "C:\...\...")
2.  use the normal / ("C:/.../..")
3.  use the \\ ("C:\\...\\...")

The images should be with .jpg or .png extension.
The Json file should be with .json extension.

Make sure you have the correct permissions.
"""


def test_create_directory():
    """Create a testing_io directory.

    Returns:
        string : path to testing_io directory.
    """
    current_path = os.getcwd()
    new_path_dir = os.path.join(current_path, "testing_io")
    os.mkdir(new_path_dir)
    assert new_path_dir.endswith("testing_io")


def test_load_image_none():
    """Testing if the image was loaded."""
    image = io.load_image(os.getcwd() + "\\testing_io\\test.png")
    assert image is None, "should not be None, the image doens't exist."


def test_save_image():
    """Testing the saving of an image."""
    image = np.zeros((2, 2, 3), dtype=np.float32)
    save = io.save_image(os.getcwd() + "\\testing_io\\test.png", image)
    assert save is True, "Image not saved."


def test_load_image():
    """Testing the loading of the image."""
    image = io.load_image(os.getcwd() + "\\testing_io\\test.png")
    assert image.shape == (2, 2, 3)


def test_load_json_none():
    """Testing the loading of a non existing json (should raise an error)."""
    with pytest.raises(Exception):
        io.load_json(os.getcwd() + "\\testing_io\\test.json")


def test_save_json():
    """Testing the saving of a dictionnary into a .json file."""
    data = {"test": "this is a test"}
    save = io.save_json(os.getcwd() + "\\testing_io\\test.json", data)
    assert save is True, "json not saved."


def test_load_json():
    """Testing the loading of the .json file."""
    data = io.load_json(os.getcwd() + "\\testing_io\\test.json")
    assert data == {"test": "this is a test"}


def test_load_image_data():
    """Testing the loading of both image and .json file."""
    image_data = io.load_image_data(os.getcwd() + "\\testing_io\\test.json")
    image = image_data["image"]
    del image_data["image"]
    assert image.shape == (2, 2, 3) and image_data == {"test": "this is a test"}


def test_save_image_data():
    """Testing the saving of both image and data of the image into a .png and .json file."""
    image_data = {
        "test": "this is a test",
        "image": np.zeros((2, 2, 3), dtype=np.float32),
    }

    io.save_image_data(image_data, os.getcwd() + "\\testing_io\\test2.json")
    image_data_copy = io.load_image_data(os.getcwd() + "\\testing_io\\test2.json")

    assert (
        image_data["image"].shape == image_data_copy["image"].shape
        and image_data["test"] == image_data_copy["test"]
    )


def test_delete_directory():
    """Deletes the created directory."""
    path_dir = os.path.join(os.getcwd(), "testing_io")
    files_to_delete = glob(os.path.join(path_dir, "*"))

    for filepath in files_to_delete:
        os.remove(filepath)

    os.rmdir(path_dir)
    assert os.path.exists(path_dir) is False
