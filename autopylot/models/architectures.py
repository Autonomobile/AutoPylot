"""This is where we will store our different model architectures."""

import logging

from keras_flops import get_flops
from tensorflow.keras import Input, Model
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


def shape_flatten(shape):
    """Get the number of dense neurons required the given shape.

    Args:
        shape (iterable): the shape of the output

    Returns:
        int: the number of dense neurons.
    """
    tot = 1
    for n in shape:
        tot *= n
    return tot


def test_model(output_layers=[("steering", (1,))]):
    """This model does nothing, it's just a dummy model to test our functions.

    We should respect the main structure of this function,
    But the parameters, inputs and outputs may vary: we can hardcode inputs and outputs if we want.

    Args:
        outputs (list): list of tuple containing the name and the shape of the output.
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
        y = Dense(shape_flatten(shape), name=name)(x)
        outputs.append(y)

    # Create the model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile it
    model.compile(optimizer="adam", loss="mse")

    # Get the number of floating operations required to run the model
    # logging.info(f"created test_model with {get_flops(model)} FLOPS")
    return model


def steering_model():
    inputs = []
    outputs = []

    inp = Input(shape=(120, 160, 3), name="image")
    inputs.append(inp)

    x = Cropping2D(cropping=((40, 0), (0, 0)))(inp)
    x = BatchNormalization()(x)
    x = Conv2D(8, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
    x = Conv2D(16, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
    x = Conv2D(24, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
    x = Conv2D(32, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
    x = Conv2D(48, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)

    x = Flatten()(x)
    x = Dropout(0.4)(x)
    x = Dense(100, use_bias=False, activation="relu")(x)
    x = Dense(50, use_bias=False, activation="relu")(x)

    y = Dense(1, use_bias=False, activation="linear", name="steering")(x)
    outputs.append(y)

    # Create the model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile it
    model.compile(optimizer="adam", loss="mse")

    return model
