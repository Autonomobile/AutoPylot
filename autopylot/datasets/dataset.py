""" Here we will load and save dataset."""

import glob
import os
from ..utils import io


def load_dataset(dirpath):
    """load dataset (json and png from a folder).
        *ps glob.glob gives a list of path.
    Args:
        dirpath (string): path of a directory which contains json and png.
    Returns:
        list[dict]: list of dictionnary containing image and json.
    """
    datas = []
    for filepath in glob.glob(dirpath + "*.json"):
        datas.append(io.load_image_data(filepath))
    return datas


def load_multiple_dataset(dirpaths, flat=False):
    """load multiple dataset
    Args:
        dirpaths (string): string to multiple folders
    Returns:
        list[list[dict]] : loaded data.
    """
    datas = []
    for dirpath in glob.glob(dirpaths):
        if flat:
            datas += load_dataset(dirpath)
        else:
            datas.append(load_dataset(dirpath))
    return datas


def load_dataset_generator(dirpath):
    """Load dataset generator.
    Args:
        dirpath (string): path of directory which contains json and png.
    Returns:
        list[dict]: list of dictionnary containing image and json.
    """
    for filepath in glob.glob(dirpath + "*.json"):
        yield io.load_image_data(filepath)


""" Some usage examples :
load_multiple_dataset(".", False)  # list of list
load_multiple_dataset(".", True)  # 1 list
for image_data in load_dataset_generator("dataset\\car\\"):
   dosomething(image_data) 
"""


def load_sorted_dataset(dirpath):
    """Load sorted data.
    Args:
        dirpath (string): path of directory which contains sorted dataset (time.png and time.json) .
    Returns:
        list[dict]: Loaded data (in order)
    """
    return load_dataset(__sort_dataset(dirpath))


def __sort_dataset(dirpath):
    """sort dataset
    Args:
        dirpath (strign): path of directory which contains sorted dataset (time.png and time.json).
    Returns:
        list[dict]: Sorted dataset.
    """
    datas = []
    date = __get_time_stamp(dirpath)
    datas = sorted(dirpath, key=date)
    return datas


def __get_time_stamp(dirpath):
    """get time jsonfile
    Args:
        dirpath (string): path of directory which contains sorted dataset (time.png and time.json).
    Returns:
        Float: The name of the json file in float
    """
    file = os.path.basename(dirpath)
    date = file.split(".json")[0]
    return float(date)
