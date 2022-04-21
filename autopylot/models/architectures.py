"""This is where we will store our different model architectures."""

import logging
import tensorflow as tf
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


def ConNet():
    inputs = []
    outputs = []

    image_inp = Input(shape=(120, 160, 3), name="image")
    inputs.append(image_inp)

    # First layer.
    x = BatchNormalization()(image_inp)
    x = Conv2D(
        8,
        (7, 7),
        strides=(3, 3),
        padding="valid",
        activation="relu",
        use_bias=False,
        name="conv1",
    )(x)

    x = GlobalAveragePooling2D(pool_size=(4, 4), name="pool1")(x)
    print(x.get_shape())

    # Second layer.
    x = Conv2D(
        16, (5, 5), strides=(2, 2), activation="relu", use_bias=False, name="conv2"
    )(x)

    x = Conv2D(
        24, (3, 3), strides=(2, 2), activation="relu", use_bias=False, name="conv3"
    )(x)

    x = GlobalAveragePooling2D(pool_size=(3, 3), name="pool2")(x)

    # Third layer.
    x = Conv2D(
        32, (3, 3), strides=(2, 2), activation="relu", use_bias=False, name="conv4"
    )(x)

    x = Conv2D(
        48, (3, 3), strides=(1, 1), activation="relu", use_bias=False, name="conv5"
    )(x)

    x = GlobalAveragePooling2D(pool_size=(2, 2), name="pool3")(x)

    # FC aand flatten the layer.
    x = Flatten(name="flatten")(x)
    x = Dropout(0.3)(x)
    x = Dense(64, activation="relu", use_bias=False, name="fc1")(x)
    x = Dense(32, activation="relu", use_bias=False, name="fc2")(x)

    # Output layer.
    y = Dense(1, name="steering")(x)
    y = tf.keras.activations.sigmoid(y)
    outputs.append(y)

    # Get throttle
    throttle_inp = Input(shape=(1,), name="throttle")
    inputs.append(throttle_inp)

    # Create the model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile it
    model.compile(optimizer="adam", loss="mse")

    return model
