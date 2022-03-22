"""Some useful functions."""
import base64

import cv2
import numpy as np


def map_value(value, inmin, inmax, outmin, outmax):
    """Map the value to a given min and max.

    Args:
        value (number): input value.
        min (number): min input value.
        max (number): max input value.
        outmin (number): min output value.
        outmax (number): max output value.

    Returns:
        number: output value.
    """
    if value < inmin:
        value = inmin
    elif value > inmax:
        value = inmax

    return ((outmax - outmin) * (value - inmin)) / (inmax - inmin) + outmin


def deadzone(value, threshold, center=0.0):
    """Apply a deadzone to a given value centered around a center value.

    Args:
        value (number): value to apply the deadzone to.
        threshold (number): the threshold to apply.
        center (number, optional): center value. Defaults to 0.

    Returns:
        number: [description]
    """
    return value if abs(value - center) > threshold else center


def encode_image(img, encode_params=[int(cv2.IMWRITE_JPEG_QUALITY), 90]):
    _, encimg = cv2.imencode(".jpg", img, encode_params)
    return base64.b64encode(encimg).decode("utf-8")


def decode_image(encimg):
    nparr = np.frombuffer(base64.b64decode(encimg), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
