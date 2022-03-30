"""This is where we will store our different model architectures."""

import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import (
    Activation,
    BatchNormalization,
    Concatenate,
    Conv2D,
    Cropping2D,
    Dense,
    DepthwiseConv2D,
    Dropout,
    Flatten,
    GlobalAveragePooling2D,
    Lambda,
    MaxPooling2D,
    Reshape,
    SeparableConv2D,
)


def get_number_of_neurons(shape):
    """Get the number of dense neurons for the given shape.

    Args:
        shape (iterable): the shape of the output

    Returns:
        int: the number of dense neurons.
    """
    tot = 1
    for n in shape:
        tot *= n
    return tot


def test_model(output_layers: dict):
    """This model does nothing, it's just a dummy model to test our functions.

    Args:
        outputs (dict): dict containing the name and the shape of the output.
    """
    inputs = []
    outputs = []

    inp = Input(shape=(120, 160, 3), name="image")
    inputs.append(inp)
    x = GlobalAveragePooling2D()(inp)

    inp2 = Input(shape=(1), name="speed")
    inputs.append(inp2)
    x = Concatenate()([x, inp2])

    for (name, shape) in output_layers:
        y = Dense(get_number_of_neurons(shape), name=name)(x)
        outputs.append(y)

    return tf.keras.models.Model(inputs=inputs, outputs=outputs)
