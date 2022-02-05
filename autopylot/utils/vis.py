import cv2
import numpy as np


def vis_line_scalar(
    image,
    scalar,
    pos=(1, 0.5),
    length=(0.25, 0),
    fact=(1, 0),
    color=(0, 0, 255),
    thickness=2,
):
    """Visualize a scalar as a line.

    Args:
        image (np.array): the image.
        scalar (scalar): the scalar.
        pos (iterable, optional): y and x coordinates (between 0 and 1). Defaults to np.array([1, 0.5]).
        length (iterable, optional): y_length and x_length of the line (between 0 and 1). Defaults to np.array([0.25, 0]).
        color (tuple, optional): color of the line to draw. Defaults to [255, 255, 255].
        thickness (int, optional): thickness of the line to draw. Defaults to 2.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    h, w, _ = image.shape

    p1 = (
        int(pos[0] * h),
        int(pos[1] * w),
    )
    p2 = (
        int(pos[0] * h + fact[0] * scalar * length[0] * h),
        int(pos[1] * w + fact[1] * scalar * length[1] * w),
    )
    vis_image = cv2.line(image, p1, p2, color, thickness)
    return vis_image


def vis_steering(image_data):
    """Visualize the steering scalar.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_line_scalar(
        image_data["image"],
        image_data["steering"],
        pos=(1, 0.5),
        length=(0.2, 0.2),
        fact=(0, 1),
        color=(0, 0, 255),
        thickness=2,
    )


def vis_throttle(image_data):
    """Visualize the throttle scalar.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_line_scalar(
        image_data["image"],
        image_data["throttle"],
        pos=(1, 0.9),
        length=(0.2, 0),
        fact=(1, 0),
        color=(0, 0, 255),
        thickness=2,
    )


def vis_speed(image_data):
    """Visualize the speed scalar.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_line_scalar(
        image_data["image"],
        image_data["speed"],
        pos=(1, 0.9),
        length=(0.2, 0),
        fact=(1, 0),
        color=(255, 0, 0),
        thickness=2,
    )


def vis_point(image, point, color=(0, 0, 255), radius=2):
    """Visualize a two dimension data.

    Args:
        image (np.array): the image.
        point (tuple, np.array, list): the point to plot.
        color (tuple, optional): color of the point to draw. Defaults to (0, 0, 255).
        radius (int, optional): size of the point to draw. Defaults to 2.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return cv2.circle(image, point, radius, color, thickness=-1)


def vis_car_position(image_data):
    """Visualize the position of the detected car.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_point(image_data["image"], image_data["car_position"])
