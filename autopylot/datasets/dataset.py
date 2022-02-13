""" Here we will load and save dataset."""
import glob
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


""" Some usage examples

load_multiple_dataset(".", False)  # list of list
load_multiple_dataset(".", True)  # 1 list

for image_data in load_dataset_generator("dataset\\car\\"):
   dosomething(image_data) 

"""
