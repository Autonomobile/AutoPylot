""" Here we will load and save data""" 
from PIL import Image 
from numpy import asarray

def load_image(path): #Should return the image as array.
    image = PImage.open(path)
    array_data = asarray(image)
    return array_data


print (load_images("C:\\Users\\sacha\\Pictures\\Saved Pictures\\1")) #testing if wokring

def save_image(path):


def laod_json(path):


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
