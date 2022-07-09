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
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.optimizers import Adam, SGD


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


def sort_input_outputs(inputs, outputs):
    """Sort in the alphabetic order input and output so that
    the tflite model will have the same input and output order.

    Args:
        inputs (list): list of input tensors
        outputs (list): list of output tensors
    """
    inputs = sorted(inputs, key=lambda x: x.name)
    outputs = sorted(outputs, key=lambda x: x.name)
    return inputs, outputs


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
        inputs, outputs = sort_input_outputs(inputs, outputs)
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

    def ConvNet():
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
        x = Conv2D(32, 3, strides=2, activation="relu", use_bias=False, name="conv4")(x)
        x = Conv2D(48, 3, strides=2, activation="relu", use_bias=False, name="conv5")(x)
        # x = AveragePooling2D(pool_size=2, name="pool3")(x)

        # Fourth layer.
        x = Conv2D(64, 3, strides=2, activation="relu", use_bias=False, name="conv7")(x)
        # x = AveragePooling2D(pool_size=2, name="pool4")(x)

        # FC aand flatten the layer.
        x = Flatten(name="flatten")(x)
        x = Dropout(0.3)(x)
        x = Dense(200, activation="relu", use_bias=False, name="fc1")(x)
        x = Dense(80, activation="relu", use_bias=False, name="fc2")(x)

        # Output layer.
        y = Dense(1, name="steering", activation="tanh")(x)
        outputs.append(y)

        speed = Input(shape=(1,), name="speed")
        inputs.append(speed)
        x = Concatenate(axis=-1)([x, speed])

        x = Dense(100, activation="elu")(x)
        x = Dropout(0.2)(x)
        x = Dense(50, activation="elu")(x)

        y = Dense(1, activation="sigmoid", name="throttle")(x)
        outputs.append(y)

        # Create the model
        inputs, outputs = sort_input_outputs(inputs, outputs)
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
        x = Lambda(lambda x: x / 255)(x)

        x = Conv2D(12, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Conv2D(24, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Conv2D(32, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Conv2D(48, 3, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Conv2D(64, 3, strides=1, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = Flatten()(x)
        x = Dropout(0.2)(x)

        x = Dense(200, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dense(100, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dense(100, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dropout(0.1)(x)

        y1 = Dense(1, use_bias=False, activation="tanh", name="steering")(x)
        outputs.append(y1)

        y2 = Dense(3, use_bias=False, activation="softmax", name="zone")(x)
        outputs.append(y2)

        # Create the
        inputs, outputs = sort_input_outputs(inputs, outputs)
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(optimizer=Adam(), loss="mse", loss_weights=[1, 0.75])

        logging.info(f"created gigachad model with {get_flops(model)} FLOPS")
        return model

    def Max_model():
        inputs = []
        outputs = []

        inp = Input(shape=(120, 160, 3), name="image")
        inputs.append(inp)

        x = Cropping2D(cropping=((40, 0), (0, 0)))(inp)
        x = BatchNormalization()(x)

        x = Conv2D(4, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
        x = Conv2D(8, kernel_size=5, strides=2, use_bias=False, activation="relu")(x)
        x = Conv2D(16, kernel_size=3, strides=2, use_bias=False, activation="relu")(x)

        x = Conv2D(32, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
        x = Conv2D(48, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)
        x = Conv2D(64, kernel_size=3, strides=1, use_bias=False, activation="relu")(x)

        x = Flatten()(x)  # construct vector from the matrix
        x = Dropout(0.4)(x)
        x = Dense(100, use_bias=False, activation="relu")(x)
        x = Dense(50, use_bias=False, activation="relu")(x)

        y = Dense(1, use_bias=False, activation="tanh", name="steering")(x)
        outputs.append(y)

        # Create the model
        inputs, outputs = sort_input_outputs(inputs, outputs)
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(
            optimizer="adam", loss="mse"
        )  # can change the optimizer adam by stg else

        return model

    def separable_model():
        inputs = []
        outputs = []

        inp = Input(shape=(120, 160, 3), name="image")
        inputs.append(inp)

        x = Cropping2D(cropping=((20, 20), (0, 0)))(inp)
        x = Lambda(lambda x: x / 255)(x)

        x = SeparableConv2D(24, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(48, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(96, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(192, 3, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(256, 3, strides=1, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = Flatten()(x)
        x = Dropout(0.3)(x)

        x = Dense(200, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dense(100, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dense(100, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        # make sure the outputs are in alphabetic order
        y1 = Dense(1, use_bias=False, activation="tanh", name="steering.0")(x)
        outputs.append(y1)
        y2 = Dense(1, use_bias=False, activation="tanh", name="steering.5")(x)
        outputs.append(y2)
        y3 = Dense(1, use_bias=False, activation="tanh", name="steering.10")(x)
        outputs.append(y3)
        z = Dense(3, use_bias=False, activation="softmax", name="zone")(x)
        outputs.append(z)

        # Create the model
        inputs, outputs = sort_input_outputs(inputs, outputs)
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(optimizer=Adam(), loss="mse", loss_weights=[1, 1, 1, 0.75])

        logging.info(f"created gigachad model with {get_flops(model)} FLOPS")
        return model

    def trajectory_model():
        inputs = []
        outputs = []

        inp = Input(shape=(120, 160, 3), name="image")
        inputs.append(inp)

        x = Cropping2D(cropping=((20, 20), (0, 0)))(inp)
        x = Lambda(lambda x: x / 255)(x)

        x = SeparableConv2D(24, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(48, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(96, 5, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(192, 3, strides=2, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(256, 3, strides=1, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)

        x = Flatten()(x)
        x = Dropout(0.3)(x)

        x = Dense(200, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dropout(0.1)(x)

        x = Dense(200, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dropout(0.1)(x)

        x = Dense(200, use_bias=False)(x)
        x = Activation("relu")(x)
        x = BatchNormalization()(x)
        x = Dropout(0.1)(x)

        # make sure the outputs are in alphabetic order
        y1 = Dense(1, use_bias=False, activation="tanh", name="steering.0")(x)
        outputs.append(y1)
        y3 = Dense(1, use_bias=False, activation="tanh", name="steering.5")(x)
        outputs.append(y3)
        y4 = Dense(20, use_bias=False, activation="linear", name="trajectory")(x)
        outputs.append(y4)
        y5 = Dense(3, use_bias=False, activation="softmax", name="zone")(x)
        outputs.append(y5)

        # Create the model
        inputs, outputs = sort_input_outputs(inputs, outputs)
        model = Model(inputs=inputs, outputs=outputs)

        # Compile it
        model.compile(
            optimizer=Adam(),
            loss=["mse", "mse", "mse", "categorical_crossentropy"],
            loss_weights=[1, 1, 1.5, 0.75],
        )

        logging.info(f"created gigachad model with {get_flops(model)} FLOPS")
        return model

    def mmms():
        inputs = []
        outputs = []

        image = Input(shape=(120, 160, 3), name="image")
        speed = Input(shape=(1,), name="speed")

        inputs.append(image)
        inputs.append(speed)

        x = Cropping2D(cropping=((20, 20), (0, 0)))(image)
        x = Lambda(lambda x: x / 255)(x)

        x = SeparableConv2D(24, 5, strides=2, use_bias=False, activation="relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(48, 5, strides=2, use_bias=False, activation="relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(96, 5, strides=2, use_bias=False, activation="relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(192, 3, strides=2, use_bias=False, activation="relu")(x)
        x = BatchNormalization()(x)

        x = SeparableConv2D(256, 3, strides=1, use_bias=False, activation="relu")(x)
        x = BatchNormalization()(x)

        x = Flatten()(x)
        x = Dropout(0.3)(x)
        x = Concatenate(axis=-1)([x, speed])

        x = Dense(256, use_bias=False, activation="relu")(x)
        x = Dropout(0.3)(x)
        x = BatchNormalization()(x)

        x = Dense(256, use_bias=False, activation="relu")(x)
        x = Dropout(0.3)(x)
        x = BatchNormalization()(x)

        x = Dense(256, use_bias=False, activation="relu")(x)
        x = Dropout(0.3)(x)
        x = BatchNormalization()(x)

        y1 = Dense(1, use_bias=False, activation="tanh", name="steering.0")(x)
        y2 = Dense(1, use_bias=False, activation="tanh", name="steering.5")(x)
        y3 = Dense(1, use_bias=False, activation="tanh", name="steering.10")(x)
        z = Dense(3, use_bias=False, activation="softmax", name="zone")(x)

        outputs.append(y1)
        outputs.append(y2)
        outputs.append(y3)
        outputs.append(z)

        inputs, outputs = sort_input_outputs(inputs, outputs)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer="adam", loss="mse", loss_weights=[1, 1, 1, 0.75])

        logging.info(f"created model with {get_flops(model)} FLOPS")
        return model
