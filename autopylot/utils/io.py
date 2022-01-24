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

# path is the path to the json file.
def load_json(path):
    with open(os.path.normpath(path), "r") as json_file:
        return json.load(json_file)

# saving the json file.

def load_both (json_path): #load image associate to json file
    json_data = json.load(json_path) #path of the json file
    image_path = cv2.imread(json_path) #deduce the path of the image 
    image = cv2.imread(image_path) #load image .png
    return image, json_data

def save_json(path, to_save):
    with open(os.path.normpath(path), "w") as json_file:
        return json.dump(to_save, path)


#def load_both (json_path):
