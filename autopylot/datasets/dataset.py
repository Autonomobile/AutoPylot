"""
Here we will load and save dataset.

Some usage examples :
load_multiple_dataset(".", False)  # list of list
load_multiple_dataset(".", True)  # 1 list
for image_data in load_dataset_generator("dataset\\car\\"):
    dosomething(image_data) 
"""

import glob
import os
from ..utils import io


def __get_time_stamp(path):
    """Get time component of the jsonfile.

    Args:
        path (string): path of a json file.
    Returns:
        Float: The name of the json file in float
    """
    return float(os.path.basename(path).split(".json")[0])


def get_every_json_paths(dirpath):
    """Get every json path.

    Args:
        dirpath (string): path of directory which contains json and png.
    Returns:
        list[string]: List of json path.
    """
    return glob.glob(os.path.join(dirpath, "**", "*.json"), recursive=True)


def sort_paths(paths):
    """Sort paths.

    Args:
        paths (list[string]): json file path.
    Returns:
        list[string]: Sorted paths.
    """
    return sorted(paths, key=__get_time_stamp)


def sequence_sorted_paths(dirpath, split_time=2):
    """Sequence sorted paths.

    Args:
        dirpath (string): path of directory containing json and png files.
    Returns:
        list[list[string]]: List of sequences of sorted paths.
    """
    paths = sort_paths(get_every_json_paths(dirpath))
    seq_paths = [[]]
    for i in range(1, len(paths)):
        if __get_time_stamp(paths[i]) - __get_time_stamp(
            paths[i - 1]
        ) > split_time or os.path.dirname(paths[i]) != os.path.dirname(paths[i - 1]):
            seq_paths.append([paths[i]])
        else:
            seq_paths[-1].append(paths[i])

    return seq_paths


def load_dataset(dirpath):
    """Load dataset (json and png from a folder).

    Args:
        dirpath (string): path of a directory which contains json and png.
    Returns:
        list[dict]: list of dictionnary containing image and json.
    """
    datas = []
    for filepath in glob.glob(dirpath + os.sep + "*.json"):
        datas.append(io.load_image_data(filepath))
    return datas


def load_multiple_dataset(dirpath, flat=False):
    """Load multiple dataset

    Args:
        dirpath (string): path of a directory containing other directories that contain json and png.
        flat(bool, optional): if True, returns list[dict]
    Returns:
        list[list[dict]] : loaded data.
    """
    datas = []
    for path in glob.glob(dirpath + os.sep + "*"):
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
    Yields:
        list[dict]: list of dictionnary containing image and json.
    """
    for filepath in glob.glob(dirpath + os.sep + "*.json"):
        yield io.load_image_data(filepath)


def load_multiple_dataset_generator(dirpath, flat=False):
    """Load multiple dataset generator.

    Args:
        dirpath (string): path of a directory containing other directories that contain json and png.
        flat (bool, optional):  if True, returns list[dict].

    Yields:
        list[list[dict]]: list of list of dictionnary containing image and json.
    """
    for path in glob.glob(dirpath + os.sep + "*"):
        if os.path.isdir(path):
            if flat:
                for data in load_dataset_generator(path):
                    yield data
            else:
                yield load_dataset_generator(path)


def load_sorted_dataset(dirpath):
    """Load sorted data.

    Args:
        dirpath (string): path of directory which contains sorted dataset (time.png and time.json) .
    Returns:
        list[dict]: Loaded data (in order)
    """
    datas = []
    for filepath in sort_paths(glob.glob(dirpath + os.sep + "*.json")):
        datas.append(io.load_image_data(filepath))
    return datas


def load_multiple_sorted_dataset(dirpath, flat=False):
    """Load multiple sorted dataset.

    Args:
        dirpath (string): path of a directory containing other directories that contain json and png.
        flat (bool, optional):  if True, returns list[dict].

    Returns:
        list[list[dict]]: sorted data.
    """
    datas = []
    for path in glob.glob(dirpath + os.sep + "*"):
        if os.path.isdir(path):
            if flat:
                datas += load_sorted_dataset(path)
            else:
                data = load_sorted_dataset(path)
                if data != []:
                    datas.append(data)
    return datas


def load_sorted_dataset_generator(dirpath):
    """Load sorted dataset generator.

    Args:
        dirpath (string): path of directory which contains json and png.
    Returns:
        list[dict]: list of dictionnary containing image and json.
    """
    for filepath in sort_paths(glob.glob(dirpath + os.sep + "*.json")):
        yield io.load_image_data(filepath)


def load_multiple_sorted_dataset_generator(dirpath, flat=False):
    """Load multiple sorted dataset generator.

    Args:
        dirpath (string): path of a directory containing other directories that contain json and png.
        flat (bool, optional):  if True, yields list[dict].
    Yields:
        list[list[dict]]: list of dictionnary containing image and json.
    """
    for path in glob.glob(dirpath + os.sep + "*"):
        if os.path.isdir(path):
            if flat:
                for data in load_sorted_dataset_generator(path):
                    yield data
            else:
                yield load_sorted_dataset_generator(path)
