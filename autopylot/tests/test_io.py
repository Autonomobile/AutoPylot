"""test the io class"""
import os
#from ..utils import io

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
    current_path = os.getcwd()
    new_path_dir = os.path.join(current_path,"testing_io")
    os.mkdir(new_path_dir)
    print ("Test directory created successfully here :", new_path_dir)
    return new_path_dir

#create_directory()

def delete_directory():
    path = os.getcwd()
    path_dir = os.path.join(path,"testing_io")
    os.rmdir(path_dir)
    print("succesfully removed test directory")

#delete_directory()
"""
def test_load_image():
    image = io.load_image("../.../image.jpg")
    assert image is None, "should not be None, given path no correct/not excistent."


def test_save_image():
    image = io.load_image("../.../image.jpg")
    save = io.save_image(image, "../.../saved_image.jpg")
    assert save is True, "should not be None."

def test_laod_json():
    file = io.laod_json("../.../file.json")
    assert file is None, "should not be None."

# def test_save_json():

#     assert

# def test_both():

#     assert
"""