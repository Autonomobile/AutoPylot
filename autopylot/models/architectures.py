"""This is where we will store our different model architectures."""

import logging
from pyexpat import model

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
from tensorflow.keras.regularizers import l1_l2
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

        # Create the model
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(optimizer="adam", loss="mse")

        logging.info(f"created steering model with {get_flops(model)} FLOPS")
        return model

    def gigachad_model():
        inputs = []
        outputs = []

        inp = Input(shape=(120, 160, 3), name="image")
        inputs.append(inp)

        x = Cropping2D(cropping=((20, 20), (0, 0)))(inp)
        x = BatchNormalization()(x)

        x = Conv2D(12, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Conv2D(24, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Conv2D(32, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Conv2D(48, 3, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Conv2D(64, 3, strides=1, use_bias=False)(x)
        x = Activation("relu")(x)

        x = Flatten()(x)
        x = Dropout(0.2)(x)

        x = Dense(200, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Dense(100, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Dense(100, use_bias=False)(x)
        x = Activation("relu")(x)
        x = Dropout(0.1)(x)

        y1 = Dense(1, use_bias=False, activation="tanh", name="steering")(x)
        outputs.append(y1)

        y2 = Dense(3, use_bias=False, activation="softmax", name="zone")(x)
        outputs.append(y2)

        # Create the model
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(optimizer=Adam(), loss="mse", loss_weights=[1, 0.75])

        logging.info(f"created gigachad model with {get_flops(model)} FLOPS")
        return model

    def mickaNet():
        # 1 preparing the model ========================
        inputs = []
        outputs = []

        # 2 input layer ========================
        image = Input(shape=(120, 160, 3), name="image")
        speed = Input(shape=(1,), name="speed")

        inputs.append(image)
        inputs.append(speed)

        # 3 convolutional layers ========================
        x = BatchNormalization()(image)  # normalize data
        x = Conv2D(3, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
        x = Conv2D(6, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
        x = Conv2D(12, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
        x = Conv2D(24, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
        x = Conv2D(48, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
        x = Conv2D(64, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
        x = Conv2D(72, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
        x = Conv2D(96, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)

        # 4 flatten layer ========================
        x = Flatten()(x)  # flatten the data
        x = Dropout(0.2)(x)  # dropout to avoid overfitting

        # 5 fully connected layers ========================
        x = Concatenate(axis=-1)([x, speed])  # put inputs together
        x = Dense(100, use_bias=False, activation="relu")(x)  # layer with 100 neurons
        x = Dropout(0.1)(x)  # dropout to avoid overfitting
        x = Dense(100, use_bias=False, activation="relu")(x)
        x = Dropout(0.1)(x)

        # 6 output layer ========================
        y = Dense(1, use_bias=False, activation="tanh", name="steering")(x)
        outputs.append(y)

        # create the model
        model = Model(inputs=inputs, outputs=outputs)

        # compile the model
        model.compile(optimizer="adam", loss="mse")

        return model
