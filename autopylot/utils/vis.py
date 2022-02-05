import cv2


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
        pos=(0.5, 0),
        length=(0, 0.25),
        fact=(0.2, 0),
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
    throttle = image_data["throttle"]
    color = (0, 0, 255)
    if throttle < 0:
        color = (255, 0, 0)
        throttle *= -1

    return vis_line_scalar(
        image_data["image"],
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


def vis_speed(image_data):
    """Visualize the speed scalar.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_text_scalar(
        image_data["image"],
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


def vis_car_position(image_data):
    """Visualize the position of the detected car.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """
    return vis_point(image_data["image"], image_data["car_position"])


def vis_all(image_data):
    """Visualize every data present in the image_data dictionary.

    Args:
        image_data (dictionnary): image data dictionnary.

    Returns:
        np.array: modified image with the drawn visualization.
    """

    image_data_copy = image_data.copy()
    if "steering" in image_data_copy:
        image_data_copy["image"] = vis_steering(image_data_copy)
    if "throttle" in image_data_copy:
        image_data_copy["image"] = vis_throttle(image_data_copy)
    if "speed" in image_data_copy:
        image_data_copy["image"] = vis_speed(image_data_copy)

    return image_data_copy["image"]
