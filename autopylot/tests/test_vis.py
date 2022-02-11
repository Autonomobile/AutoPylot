import cv2
import numpy as np
import pytest

from ..utils import vis, display


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
def test_vis_compare():
    """Test the compare() vis function."""
    image_data1 = {
        "image": np.zeros((120, 160, 3), np.float32),
        "speed": 12.34,
        "steering": -0.543,
        "throttle": -0.456,
    }
    image_data2 = {
        "image": np.zeros((120, 160, 3), np.float32),
        "speed": 13.654321,
        "steering": 0.345,
        "throttle": 0.543,
    }

    vis_image = vis.compare([image_data1, image_data2], image_key="image")
    assert vis_image.shape == (120, 320, 3)
    cv2.imshow("test_vis_compare", vis_image)


@pytest.mark.vis
def test_vis_display():
    """Test some of the functions from vis combined to display."""
    image_data = {
        "image": np.zeros((120, 160, 3), np.float32),
        "speed": 12.34,
        "steering": -0.543,
        "throttle": -0.456,
    }

    disp = display.Display(
        image_data,
        ["image_disp0", "image_disp1", "image_disp2"],
        ["image", "image", "image"],
        [vis.vis_all, vis.vis_steering, display.identity_transform],
        waitKey=0,
    )

    disp.update()


def test_vis_display_wrong_params():
    """Test whether Display raises an error when giving wrong parameters."""
    with pytest.raises(Exception):
        # giving on purpose mismatched list length
        display.Display(
            {"test": "this is a test"},
            ["image_disp0", "image_disp1"],
            [],
            [display.identity_transform],
            waitKey=0,
        )
