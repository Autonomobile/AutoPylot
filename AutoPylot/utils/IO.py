""" Here we will load and save data""" 
from PIL import Image 
from numpy import asarray
import json
import cv2

def load_image(path): #Should return the image as array.
    image = PImage.open(path)
    array_data = asarray(image)
    return array_data


def save_image(path,new_path): #Save the image from the normal image
    image = PImage.open(path)
    image.save(new_path)

def save_image(path,new_path): #Probably the right version (using the numpy.array data)
    image=Image.fromarray(save_image(path))
    image.save(new_path)


def laod_json(path):#path is the path o the json file
    data = json.load(path)
    return data
    

def save_json(path):



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
