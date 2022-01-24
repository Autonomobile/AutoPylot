"""test the io class"""

from ..utils import io

"""
When on windows don't copy the path directly use one of the following ways: 
1.  use an r (raw) before the copied path (r "C:\...\...")
2.  use the normal / ("C:/.../..")
3.  use the \\ ("C:\\...\\...")

The images should be with .jpg or .png extension.
The Json file should be with .json extension.
"""

#creer un dossier 
def create_file (path):
    pass
    


def test_load_image():
    image = io.load_image("../.../image.jpg")
    assert image is None, "should not be None, given path no correct."


def test_save_image():
    image = io.load_image("../.../image.jpg")
    io.save_image(image, "../.../saved_image.jpg")
    assert io.save_image(image, '../.../saved_image.jpg') is None, "should not be None."

def test_laod_json():
    file = io.laod_json("../.../file.json")
    assert file, "should not be None."

# def test_save_json():

#     assert

# def test_both():

#     assert
