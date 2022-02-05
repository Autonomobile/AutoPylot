import cv2
import numpy as np
import pytest

from ..utils import vis


@pytest.mark.vis
def test_vis_line_scalar_positive():
    image = np.zeros((120, 160, 3), np.float32)

    vis_image = vis.vis_line_scalar(image, 0.5)
    assert not np.array_equal(vis_image, image)
    cv2.imshow("test_vis_line_scalar_positive", vis_image)


@pytest.mark.vis
def test_vis_line_scalar_negative():
    image = np.zeros((120, 160, 3), np.float32)

    vis_image = vis.vis_line_scalar(image, -0.5)
    assert not np.array_equal(vis_image, image)
    cv2.imshow("test_vis_line_scalar_negative", vis_image)


@pytest.mark.vis
def test_vis_steering_positive():
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "steering": 1.0,
    }

    vis_image = vis.vis_steering(image_data)
    assert not np.array_equal(vis_image, image_data["image"])
    cv2.imshow("test_vis_steering_positive", vis_image)


@pytest.mark.vis
def test_vis_steering_negative():
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "steering": -1.0,
    }

    vis_image = vis.vis_steering(image_data)
    assert not np.array_equal(vis_image, image_data["image"])
    cv2.imshow("test_vis_steering_negative", vis_image)


@pytest.mark.vis
def test_vis_throttle_positive():
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "throttle": 0.5,
    }

    vis_image = vis.vis_throttle(image_data)
    assert not np.array_equal(vis_image, image_data["image"])
    cv2.imshow("test_vis_throttle_positive", vis_image)


@pytest.mark.vis
def test_vis_throttle_negative():
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "throttle": -0.5,
    }

    vis_image = vis.vis_throttle(image_data)
    assert not np.array_equal(vis_image, image_data["image"])
    cv2.imshow("test_vis_throttle_negative", vis_image)


@pytest.mark.vis
def test_vis_speed():
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "speed": 13.654321,
    }

    vis_image = vis.vis_speed(image_data)
    assert not np.array_equal(vis_image, image_data["image"])
    cv2.imshow("test_vis_speed", vis_image)


@pytest.mark.vis
def test_vis_all():
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "speed": 13.654321,
        "steering": 0.345,
        "throttle": 0.543,
    }

    vis_image = vis.vis_all(image_data)
    assert not np.array_equal(vis_image, image_data["image"])
    cv2.imshow("test_vis_all", vis_image)


@pytest.mark.vis
def test_vis_display():
    """This function displays all the above cv2.imshow, to close, press any key."""
    cv2.waitKey(0)
