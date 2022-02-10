"""test the File.IO class"""
import os
import numpy as np
from glob import glob

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
    """test if the function load_dataset works.
    """
    list_of_dict = dataset.load_dataset(os.getcwd() + "\\testing_dataset\\")
    assert list_of_dict == []

# test with list of dict 
# tes with 2 json / png 


def test_delete_directory():
    """Deletes the created directory."""
    path = os.getcwd()
    path_dir = os.path.join(path, "testing_dataset")

    files_to_delete = glob(path_dir + "\\*")

    for filepath in files_to_delete:
        os.remove(filepath)

    os.rmdir(path_dir)
    assert os.path.exists(path_dir) is False