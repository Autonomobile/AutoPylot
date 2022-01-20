""" Here we will load and save data comming from the images""" 
from numpy import asarray
import json 
import cv2
import os

def path_exists(path):#test if path exists
    return os.path.exists(path)

""" the cv2.imread function will return None
if the path to the input image is invalid, but i created a function to symplify.
Path_exists can be removed, just don't forget to remove the calls to the function."""

def load_image(path): #Should return the image as array (num_rows, num_cols, num_channels).
    if path_exists(path) == True:
        array_data = cv2.imread(path)
        return array_data
    else:
        return False
    array_data.close()


def save_image(path,save_path): #Probably the right version (using the numpy.array data)
    saved = cv2.imwrite(save_path,load_image(path))
    return saved

def laod_json(path):#path is the path o the json file
    data = json.load(path)
    return data
    data.close()
    

def save_json(path):
    saved = json.dump(laod_json(path))
    return saved



def both ():



def test_load_image():

    assert 

def test_save_image():

    assert

def test_laod_json():

    assert

def test_save_json():

    assert

def test_both():

    assert
