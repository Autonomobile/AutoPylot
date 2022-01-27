"""test the io class"""
import os

from numpy import empty
from ..utils import io

"""
When on windows don't copy the path directly use one of the following ways: 
1.  use an r (raw) before the copied path (r "C:\...\...")
2.  use the normal / ("C:/.../..")
3.  use the \\ ("C:\\...\\...")

The images should be with .jpg or .png extension.
The Json file should be with .json extension.

Make sure you have the correct permissions.
"""
#create a test_io directory which will be deleted afterwards.



def create_directory():
    """create a testing_io directory 

    Returns:
        string : path to testing_io directory.
    """
    current_path = os.getcwd()
    new_path_dir = os.path.join(current_path,"testing_io")
    assert os.path.exists(new_path_dir) is True, "file already exists"
    os.mkdir(new_path_dir)
    #print ("Test directory created successfully here :", new_path_dir)
    return new_path_dir


def delete_directory():
    """ deletes the created directory.
    """

    path = os.getcwd()
    path_dir = os.path.join(path,"testing_io")
    os.rmdir(path_dir)
    #print("successfully removed test directory")


def test_load_image():
    """testing if the image was 
    """
    #dir = create_directory()
    image = io.load_image("C:\\Users\\maxim\\Desktop\\Projet S2" + "logo2.png")
    assert image is None, "should not be None, given path no correct/not excistent."
    #delete_directory()


def test_save_image():
    #dir = create_directory()
    image = io.load_image("C:\\Users\\maxim\\Desktop\\Projet S2\\logo2.png")
    save = io.save_image("C:\\Users\\maxim\\Desktop\\Projet S2\\test\\logo3.png", image)
    assert save is True, "Image not saved."
    #delete_directory()


def test_load_json():
    """need to change assert to have stg good
    """
    data = io.load_json("C:\\Users\\maxim\\Desktop\\Projet S2\\test\\test.json")
    #delete_directory()
    assert data != {}, "given file does not exist" 
    


def test_save_json():
    #dir = create_directory()
    data = io.load_json("C:\\Users\\maxim\\Desktop\\Projet S2\\test\\test.json")
    save = io.save_json("C:\\Users\\maxim\\Desktop\\Projet S2\\test\\test2.json", data)
    assert save is None, "Image not saved."
    #delete_directory()

def test_save_image_data():
    pass

def test_load_image_data ():  
    pass