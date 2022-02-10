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
    list = []
    for file in glob.glob(dirpath + "*.json") :
        list.append(io.load_image_data(file))
    return list


def load_multiple_dataset(dirpaths, flat=False):
    """load multiple dataset 

    Args:
        dirpaths (string): string to multiple folders

    Returns:
        list of list of dictionnary: is a simple list of dictionnary good ? 
    """
    list = []
    for dir in glob.glob(dirpaths) :
        if flat:
            list += load_dataset(dir)
        else:
            list.append(load_dataset(dir))
    return list

load_multiple_dataset(".", False) # list of list 
load_multiple_dataset(".", True) # 1 list