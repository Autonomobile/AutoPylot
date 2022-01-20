""" Here we will load and save data comming from the images""" 
from numpy import asarray
import json 
import cv2
import os


def load_image(path): #Should return the image as array (num_rows, num_cols, num_channels).
    return cv2.imread(path)


def save_image(path,save_path): #Probably the right version (using the numpy.array data)
    return cv2.imwrite(save_path,load_image(path))


def laod_json(path):#path is the path o the json file
    return json.load(path)
    data.close()
    

def save_json(path):
    return json.dump(laod_json(path))


def get_image_path()

def load_both (json_path):
    
