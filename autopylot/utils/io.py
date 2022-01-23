""" Here we will load and save data comming from the images""" 
from numpy import asarray
import json 
import cv2


"""When on windows don't copy the path directly use one of the following ways: 
1.  use an r (raw) before the copied path (r "C:\...\...")
2.  use the normal /
3.  use the \\ ("C:\\...\\...")
"""


def load_image(path): #Should return the image as array (num_rows, num_cols, num_channels).
    return cv2.imread(path)


def save_image(path,save_path): #Probably the right version (using the numpy.array data)
    return cv2.imwrite(save_path,load_image(path))


def laod_json(path):#path is the path to the json file.
    return json.load(path)
    

def save_json(path):#saving  the json file.
    return json.dump(laod_json(path))


def load_both (json_path): #load image associate to json file
    json_data = json.load(json_path) #path of the json file
    image_path = cv2.imread(json_path) #deduce the path of the image 
    image = cv2.imread(image_path) #load image .png
    return image, json_data

#tests will be removed
#print(load_image("C:\\Users\\sacha\\Downloads\\kid.jpg"))
#print(save_image("C:\\Users\\sacha\\Downloads\\kid.jpg","C:\\Users\\sacha\\Desktop\\copied image\\imagesave.jpg"))
