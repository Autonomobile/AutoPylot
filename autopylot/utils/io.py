""" Here we will load and save data comming from the images""" 
from numpy import asarray
import json 
import cv2

#Should return the image as array (num_rows, num_cols, num_channels).
def load_image(path): 
    return cv2.imread(path)

 #saves an image using the numpy.array data
def save_image(path, save_path):
    return cv2.imwrite(save_path, load_image(path))

#path is the path to the json file.
def laod_json(path):
    return json.load(path)
    
#saving the json file. (not working)
def save_json(path):
    return json.dump(laod_json(path))


#def load_both (json_path):
