""" Here we will load and save dataset."""

import glob
import os
from ..utils import io


def __sort_paths(paths):
    """sort paths
    Args:
        paths (list[string]): path of directory which contains sorted dataset (time.png and time.json).
    Returns:
        list[string]: Sorted paths.
    """
    return sorted(paths, key=__get_time_stamp)


def __get_time_stamp(path):
    """get time jsonfile
    Args:
        path (string): path of directory which contains sorted dataset (time.png and time.json).
    Returns:
        Float: The name of the json file in float
    """
    file = os.path.basename(path)
    date = file.split(".json")[0]
    return float(date)


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


def load_multiple_dataset(dirpath, flat=False):
    """load multiple dataset
    Args:
        dirpath (string): path to folder.
        flat(bool, optional): if True, returns list[dict]
    Returns:
        list[list[dict]] : loaded data.
    """
    datas = []
    for path in glob.glob(dirpath + "*"):
        if os.path.isdir(path):
            if flat:
                datas += load_dataset(path)
            else:
                data = load_dataset(path)
                if data != []:
                    datas.append(data)
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
    return load_dataset(__sort_paths(dirpath))


def load_multiple_sorted_dataset(dirpath):
    """Load multiple sorted dataset

    Args:
        dirpath (string): path of directory which contains json and png.

    Returns:
       lsit[lsit[dict]]: sorted data.
    """
    return load_multiple_dataset(__sort_paths(dirpath))


def load_multiple_data_set_generator(dirpath, flat=False):
    """loads multiple dataset generator

    Args:
        dirpath (string): path to directory which contains paths with json and png files.
        flat (bool, optional):  if True, returns list[dict] (do the thing to check if none empty).

    Yields:
        list[list[dict]]: list of list of dictionnary containing image and json.
    """
    for path in glob.glob(dirpath + "*"):
        if os.path.isdir(path):
            if flat:
                for data in load_dataset_generator(path):
                    yield data
            else:
                yield load_dataset_generator(path)
