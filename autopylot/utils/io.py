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

def load_json(path):
    """Load a json file

    Args:
        path (string): path of the json file to load

    Returns:
        dictionary: data about the image 
    """
    with open(os.path.normpath(path), "r") as json_file:
        data = json.load(json_file)
    return data 

#print(load_json("C:\\Users\\maxim\\Desktop\\Projet S2\\test\\test.json"))
def save_image(path, image):
    """Save an image to a file.

    Args:
        path (string): path of the saved image.
        image (np.array): the image to save.

    Returns:
        bool: wether the image is saved or not.
    """
    image = cv2.imwrite(path, image)
    return image

def save_json(path, to_save):
    """Save the Json file

    Args:
        path (string): path of where we want to save it
        to_save (string): is the file to save

    Returns:
        dictionary: save data about the image at the path "path"
    """
    with open(os.path.normpath(path), "w") as json_file:
        ret = json.dump(to_save, json_file)
    return ret

  
def save_image_data(image_data, path):
    """takes a dictionary (image_data), save image and json_path

    Args:
        image_data (dictionary): contains an image and json_path
        path (path): path of where we have to save those data

    Returns:
        tuple: image and data 
    """
    image = image_data["image"]
    del image_data["image"]
    return cv2.imwrite(path, image), json.dump(path, image_data)


def load_image_data (json_path):
    """load a json file and an image 

    Args:
        json_path (string): path of the json file 

    Returns:
        tuple: image and json file
    """
    image_path = json_path.split(".json")[0] + ".png"
    image_data = load_json(json_path)
    image_data["image"] = load_image(image_path)
    return image_data
    
