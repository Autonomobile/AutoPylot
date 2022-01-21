""" Here we will load and save data comming from the images""" 
from numpy import asarray
import json 
import cv2


def load_image(path): #Should return the image as array (num_rows, num_cols, num_channels).
    return cv2.imread(path)


def save_image(path,save_path): #Probably the right version (using the numpy.array data)
    return cv2.imwrite(save_path,load_image(path))


def laod_json(path):#path is the path to the json file.
    return json.load(path)
    

def save_json(path):#saving  the json file.
    return json.dump(laod_json(path))


#def load_both (json_path):

#tests will be removed
#print(load_image("C:\\Users\\sacha\\Downloads\\kid.jpg"))
#print(save_image("C:\\Users\\sacha\\Downloads\\kid.jpg","C:\\Users\\sacha\\Desktop\\copied image\\imagesave.jpg"))
