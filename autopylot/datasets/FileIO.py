""" Here we will load and save dataset."""
import os
import json
import cv2
import glob 
from ..utils import io


def load_dataset(dirpath):
    """load dataset (json and png from a folder).
        *ps glob.glob gives a list of path.

    Args:
         dirpath (string): path of a directory which contains json and png.

    Returns:
         list of dictionnary: list of tuple image an json.
    """
    files = glob.glob(dirpath + "**/*.json") 
    list = []
    for file in files :
        list.append(io.load_image_data(file))
    return list

def load_multiple_dataset(dirpaths):
    pass
    
