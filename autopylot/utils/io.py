""" Here we will load and save data comming from the images."""
import json
import cv2
import os
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Special json encoder for numpy types"""

    def default(self, obj):
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def load_image(image_path):
    """Loads an image from a path.

    Args:
        image_path (string): path of the image to load.

    Returns:
        np.array: the image.
    """
    return cv2.imread(image_path)


def load_json(json_path):
    """Loads a json file

    Args:
        json_path (string): path of the json file to load

    Returns:
        dictionary: dictionnary of the content of a json file.
    """
    with open(os.path.normpath(json_path), "r") as json_file:
        data = json.load(json_file)
    return data


def save_image(path, image):
    """Saves an image to a file.

    Args:
        path (string): path of the saved image.
        image (np.array): the image to save.

    Returns:
        bool: wether the image is saved or not.
    """
    image = cv2.imwrite(path, image)
    return image


def save_json(json_path, to_save):
    """Saves the Json file

    Args:
        json_path (string): path of where we want to save it.
        to_save (dictionnary): is the dictionnary to save.
    """
    with open(os.path.normpath(json_path), "w") as json_file:
        json.dump(to_save, json_file, cls=NumpyEncoder)
    return True


def save_image_data(image_data, json_path):
    """takes a dictionary (image_data), save image and json_path

    Args:
        image_data (dictionary): contains an image and json_path.
        json_path (path): path of where we have to save those data.

    Returns:
        bool: ret of save_image.
    """
    image_path = json_path.split(".json")[0] + ".png"

    image_data_copy = image_data.copy()
    image = image_data_copy["image"]
    del image_data_copy["image"]

    return save_image(image_path, image), save_json(json_path, image_data_copy)


def load_image_data(json_path):
    """loads a json file and an image

    Args:
        json_path (string): path of the json file.

    Returns:
        dictionnary: image and json file into a dictionary.
    """
    image_path = json_path.split(".json")[0] + ".png"
    image_data = load_json(json_path)
    image_data["image"] = load_image(image_path)
    return image_data
