import context
from cameras import camera


def test_dummy_capture():
    shape = (160, 120, 3)
    cam = camera.Camera(camera_type="dummy", shape=shape)
    img = cam.read()
    assert img.shape == shape


def test_dummy_color():
    shape = (160, 120, 1)
    cam = camera.Camera(camera_type="dummy", shape=shape)
    img = cam.read()
    assert img.shape == shape


def test_test():
    assert 1 == 2