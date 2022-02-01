"""Some useful functions."""


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
