import cv2
import numpy as np

from . import utils


def vis_line_scalar(
    image,
    scalar,
    pos=(0.5, 0.25),
    length=(0, 0),
    fact=(0, 0.25),
    color=(0, 0, 255),
    thickness=2,
):
    """Visualize a scalar as a line.

    Args:
        image (np.array): the image.
        scalar (scalar): the scalar.
        pos (iterable, optional): x and y coordinates (between 0 and 1). Defaults to np.array([0.5, 0.25]).
        length (iterable, optional): x_length and y_length of the line (between 0 and 1). Defaults to np.array([0, 0]).
        fact (iterable, optional): x_fact and y_fact of the line (between 0 and 1). Defaults to np.array([0, 0.25]).
        color (tuple, optional): color of the line to draw. Defaults to [0, 0, 255].
        thickness (int, optional): thickness of the line to draw. Defaults to 2.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    h, w, _ = image.shape

    p1 = (
        int(pos[0] * w),
        int(h - pos[1] * h),
    )
    p2 = (
        int(pos[0] * w + (fact[0] * scalar + length[0]) * w),
        int(h - pos[1] * h - (fact[1] * scalar + length[1]) * h),
    )
    vis_image = cv2.line(image.copy(), p1, p2, color, thickness)
    return vis_image


def vis_steering(image_data, image_key="image", color=(0, 0, 255)):
    """Visualize the steering scalar.

    Args:
        image_data (dictionnary): image data dictionnary.
        image_key (string): image key.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_line_scalar(
        image_data[image_key],
        image_data["steering"],
        pos=(0.5, 0),
        length=(0, 0.25),
        fact=(0.2, 0),
        color=color,
        thickness=2,
    )


def vis_throttle(image_data, image_key="image", color=(0, 0, 255)):
    """Visualize the throttle scalar.

    Args:
        image_data (dictionnary): image data dictionnary.
        image_key (string): image key.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    throttle = image_data["throttle"]
    if throttle < 0:
        color = (255, 0, 0)
        throttle *= -1

    return vis_line_scalar(
        image_data[image_key],
        throttle,
        pos=(0.9, 0),
        length=(0, 0),
        fact=(0, 0.25),
        color=color,
        thickness=2,
    )


def vis_text_scalar(
    image,
    scalar,
    pos=(0.25, 0.25),
    color=(255, 255, 255),
    fontsize=1,
    thickness=2,
):
    """Visualize a scalar as a text.

    Args:
        image (np.array): the image.
        scalar ([type]): the scalar.
        pos (tuple, optional): x and y coordinates (between 0 and 1). Defaults to (0.25, 0.25).
        color (tuple, optional): color of the text. Defaults to (255, 255, 255).
        fontsize (int, optional): font size. Defaults to 1.
        thickness (int, optional): thickness. Defaults to 2.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    h, w, _ = image.shape

    p = (
        int(pos[0] * w),
        int(h - pos[1] * h),
    )

    return cv2.putText(
        image.copy(),
        "{:.1f}".format(scalar),
        p,
        cv2.FONT_HERSHEY_SIMPLEX,
        fontsize,
        color,
        thickness,
    )


def vis_speed(image_data, image_key="image"):
    """Visualize the speed scalar.

    Args:
        image_data (dictionnary): image data dictionnary.
        image_key (string): image key.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_text_scalar(
        image_data[image_key],
        image_data["speed"],
        pos=(0.0, 0.05),
        color=(255, 255, 255),
        fontsize=0.5,
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
    return cv2.circle(image.copy(), point, radius, color, thickness=-1)


def vis_trajectory(image_data, image_key="image", x_minmax=(-1, 1), y_minmax=(0, 1.5)):
    """Visualize the trajectory.

    Args:
        image_data (dict): image data dictionary.

    Returns:
        np.array: trajectory visualization image.
    """
    trajectory = image_data["trajectory"]
    h, w, _ = image_data[image_key].shape

    for i in range(len(trajectory) // 2):
        x, y = trajectory[i * 2], trajectory[i * 2 + 1]
        x = int(utils.map_value(x, x_minmax[0], x_minmax[1], 0, w))
        y = int(utils.map_value(y, y_minmax[0], y_minmax[1], h, 0))

        image_data[image_key] = vis_point(
            image_data[image_key],
            (x, y),
            color=(0, 255, 0),
            radius=5,
        )
    return image_data[image_key]


def vis_obstacles(image_data, image_key="image", x_minmax=(-1, 1), y_minmax=(-1, 1)):
    """Visualize the coordinates of the obstacles

    Args:
        image_data (dict): image data dictionary.
        image_key (str, optional): key of the image. Defaults to "image".
        x_minmax (tuple, optional): point range. Defaults to (-1, 1).
        y_minmax (tuple, optional): point range. Defaults to (-1, 1).
    """

    y, x = image_data["obstacles-coord"]
    radius = image_data["obstacles-size"]
    h, w, _ = image_data[image_key].shape

    x = int(utils.map_value(x, x_minmax[0], x_minmax[1], 0, w))
    y = int(utils.map_value(y, y_minmax[0], y_minmax[1], 0, h))

    image_data[image_key] = vis_point(
        image_data[image_key],
        (x, y),
        color=(0, 255, 0),
        radius=int(radius * 20),
    )
    return image_data[image_key]


def vis_all(image_data, image_key="image", color=(0, 0, 255)):
    """Visualize every data present in the image_data dictionary.

    Args:
        image_data (dictionnary): image data dictionnary.
        image_key (string): image key.

    Returns:
        np.array: modified image with the drawn visualization.
    """

    image_data_copy = image_data.copy()
    if "steering" in image_data_copy:
        image_data_copy[image_key] = vis_steering(image_data_copy, image_key)
    if "throttle" in image_data_copy:
        image_data_copy[image_key] = vis_throttle(image_data_copy, image_key)
    if "speed" in image_data_copy:
        image_data_copy[image_key] = vis_speed(image_data_copy, image_key)
    if "trajectory" in image_data_copy:
        image_data_copy[image_key] = vis_trajectory(image_data_copy, image_key)
    if (
        "obstacles-coord" in image_data_copy
        and "obstacles" in image_data_copy
        and image_data_copy["obstacles"] > 0.5
    ):
        image_data_copy[image_key] = vis_obstacles(image_data_copy, image_key)

    return image_data_copy[image_key]


def compare(image_datas, image_key="image"):
    """Compare the visualization of multiple images.

    Args:
        image_datas (list): list of image_data dictionnary.
        image_key (str, optional): image key. Defaults to "image".

    Returns:
        np.array: stacked images.
    """

    vis_images = []
    for image_data in image_datas:
        vis_images.append(vis_all(image_data))

    return np.concatenate(vis_images, axis=1)


def show(image, name="image", waitkey=1):
    cv2.imshow(name, image)
    if waitkey:
        cv2.waitKey(waitkey)
