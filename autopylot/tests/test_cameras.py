"""Test the cameras."""
import context
from cameras import camera


def test_dummy_capture():
    shape = (160, 120, 3)
    test_memory = {}
    cam = camera.Camera(test_memory, camera_type="dummy", shape=shape)
    cam.update()
    assert test_memory['image'].shape == shape


def test_dummy_color():
    shape = (160, 120, 1)
    test_memory = {}
    cam = camera.Camera(test_memory, camera_type="dummy", shape=shape)
    cam.update()
    assert test_memory['image'].shape == shape
