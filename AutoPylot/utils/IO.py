""" Here we will load and save data""" 
from PIL import Image 
from numpy import asarray
#from os import listdir
#not need for list of images here.

def load_image(path): #Should return the image as array.
    image = PImage.open(path)
    array_data = asarray(image)
    return array_data


print (load_images("C:\\Users\\sacha\\Pictures\\Saved Pictures\\1")) #testing if wokring