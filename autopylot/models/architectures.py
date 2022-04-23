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
    AveragePooling2D,
    GlobalAveragePooling2D,
    Lambda,
    MaxPooling2D,
    Reshape,
    SeparableConv2D,
)
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam


def get_model_constructor_by_name(name):
    return getattr(Models, name)


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


class Models:
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
        logging.info(f"created test_model with {get_flops(model)} FLOPS")
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

        y = Dense(1, use_bias=False, activation="tanh", name="steering")(x)
        outputs.append(y)

        
    def ConNet():
        inputs = []
        outputs = []

        image_inp = Input(shape=(120, 160, 3), name="image")
        inputs.append(image_inp)

        # First layer.
        x = BatchNormalization()(image_inp)
        x = Conv2D(8, 5, strides=2, activation="relu", use_bias=False, name="conv1")(x)
        # x = AveragePooling2D(pool_size=2, name="pool1")(x)

        # Second layer.
        x = Conv2D(16, 5, strides=1, activation="relu", use_bias=False, name="conv2")(x)
        x = Conv2D(24, 3, strides=2, activation="relu", use_bias=False, name="conv3")(x)
        # x = AveragePooling2D(pool_size=2, name="pool2")(x)

        # Third layer.
        x = Conv2D(32, 3, strides=1, activation="relu", use_bias=False, name="conv4")(x)
        x = Conv2D(48, 3, strides=2, activation="relu", use_bias=False, name="conv5")(x)
        # x = AveragePooling2D(pool_size=2, name="pool3")(x)

        # Fourth layer.
        x = Conv2D(64, 3, strides=1, activation="relu", use_bias=False, name="conv6")(x)
        x = Conv2D(96, 3, strides=2, activation="relu", use_bias=False, name="conv7")(x)
        # x = AveragePooling2D(pool_size=2, name="pool4")(x)

        # FC aand flatten the layer.
        x = Flatten(name="flatten")(x)
        x = Dropout(0.3)(x)
        x = Dense(200, activation="relu", use_bias=False, name="fc1")(x)
        x = Dense(100, activation="relu", use_bias=False, name="fc2")(x)

        # Output layer.
        y = Dense(1, name="steering", activation="tanh")(x)
        outputs.append(y)
        
        speed = input(shape = (1,), name = "speed")
        
        x = Concatenate(x, axis=1)([x, speed])
        x = Dense(200, activation = "relu")(x)
        x = BatchNormalization()(x)
        x = Dropout(0,2)(x)
        x = Debse(200, activation = "relu")(x)
        x = BatchNormalization()(x)
        
        y = Dense(1, actvation = "sigmoid", name = "throttle",)(x)
        outputs.append(y)
       
        # Create the model
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(optimizer="adam", loss="mse")

        # print(f"created test_model with {get_flops(model)} FLOPS")
        return model
