""" Here we will load and save dataset."""
import os
import json
import cv2
from ..utils import io


def load_dataset(dirpath):
    """load dataset not finish (I will delete the other comments in green).

    Args:
         dirpath (string): path of a directory which contains Json and png .

    Returns:
         dictionnary: tuple image an json.
    """
    topdir = "."  # top argument : need more explaination
    exten_json = ".json"  # the extension for the search
    exten_png = ".png"
    for dirpath, dirnames, files in os.walk(
        topdir
    ):  # os.walk returns 3 value, dirpath, dirnames and filenames
        for json_file_name in files:
            if json_file_name.lower().endswith(exten_json):
                load_json(
                    os.path.join(dirpath, json_file_name)
                )  # should execute the load_json fn with the path of each json file
        for png_file_name in files:
            if png_file_name.lower().endswith(exten_png):
                load_image(
                    os.path.join(dirpath, png_file_name)
                )  # should execute the load_json fn with the path of each json file


def load_multiple_dataset(dirpaths):
    pass
