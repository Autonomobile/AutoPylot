"""test the io class"""
import os
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
    image = io.load_image(create_directory()+"image.jpg")
    assert image is None, "should not be None, given path no correct/not excistent."
    delete_directory()


def test_save_image():
    image = io.load_image(create_directory() +"image.jpg")
    save = io.save_image(image, "../saved_image.jpg")
    assert save is False, "Image not saved."
    delete_directory()

def test_laod_json():
    data = io.laod_json(create_directory()+"data.json")
    assert data is None, "given file does not exist"

def test_save_json():
    data = io.load_json(create_directory()+"data.json")
    save = io.save_json(data,)

#     assert

# def test_both():

#     assert
