
"""When on windows don't copy the path directly use one of the following ways: 
1.  use an r (raw) before the copied path (r "C:\...\...")
2.  use the normal / ("C:/.../..")
3.  use the \\ ("C:\\...\\...")
"""

from ..utils import io

def test_load_image():
    image = io.load_image('/.../.../image.jpg')
    assert image is None



def test_save_image():

    assert

def test_laod_json():

    assert

def test_save_json():

    assert

def test_both():

    assert
"""