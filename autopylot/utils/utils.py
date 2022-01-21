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
