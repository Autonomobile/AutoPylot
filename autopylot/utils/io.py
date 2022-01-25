""" Here we will load and save data comming from the images."""
import json
import cv2
import os


def load_image(path):
    """Load an image from a path.

    Args:
        path (string): path of the image to load.

    Returns:
        np.array: the image.
    """
    return cv2.imread(path)


def save_image(path, image):
    """Save an image to a file.

    Args:
        path (string): path of the saved image.
        image (np.array): the image to save.

    Returns:
        bool: wether the image is saved or not.
    """
    return cv2.imwrite(path, image)


def load_json(path):
    """Load a json file

    Args:
        path ([string]): path of the json file to load

    Returns:
        [dictionary]: data about the image 
    """
    with open(os.path.normpath(path), "r") as json_file:
        return json.load(json_file)


def save_json(path, to_save):
    """Save the Json file

    Args:
        path ([string]): path of the json file
        to_save ([string]): path of where we have to save this file

    Returns:
        [dictionary]: save data about the image at the path "to_save"
    """
    with open(os.path.normpath(path), "w") as json_file:
        return json.dump(to_save, path)


def load_image_data (json_path):
    """load a json file and an image 

    Args:
        json_path ([string]): path of the json file 

    Returns:
        [tuple]: image and json file
    """
    tmp = json_path.split(".")
    tmp.pop()
    tmp.append(".png")
    image_path = ""
    for i in tmp :
        image_path += i

    with open(os.path.normpath(json_path), "r") as json_file:
        data = {
            "image" : cv2.imread(image_path),
            "json_file" :json.load(json_path)
        } 
    return data
    
