import json
import logging
import os

import tensorflow as tf
from tensorflow.keras.models import Model
import numpy as np

from ..utils import settings

settings = settings.settings


def load_model(model_path, *args, **kwargs):
    """Load a model.

    Args:
        model_path (string): model_path relative to the settings.MODELS_PATH.

    Raises:
        ValueError: raised if the model path is not valid

    Returns:
        tuple(Model, dict): the loaded model and its inputs / outputs info.
    """
    model_path = os.path.join(settings.MODELS_PATH, model_path)

    if model_path.endswith(".h5"):
        try:
            model = tf.keras.models.load_model(model_path, *args, **kwargs)
            model_info = create_model_info(model)
            model.predict = predict_decorator(
                model, model_info["inputs"], model_info["outputs"]
            )
            return model, model_info
        except OSError:
            raise ValueError(f"Invalid path to model: {model_path}")
    elif model_path.endswith(".tflite"):
        try:
            return TFLiteModel(model_path, *args, **kwargs), load_model_info(model_path)
        except OSError:
            raise ValueError(f"Invalid path to model: {model_path}")
    else:
        raise ValueError("Invalid model path")


def save_model(model, name, model_info={}):
    """Save a model in the settings.MODELS_PATH folder.

    creates a subfolder to store the .h5 / .tflite and .info files

    Args:
        model (Model): the model to save.
        name (string): the name of the model.
    """
    folder_name = os.path.join(settings.MODELS_PATH, name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # save model
    tfpath = os.path.join(folder_name, name + ".h5")
    model.save(tfpath)

    # convert and save tflite model
    tflitepath = os.path.join(folder_name, name + ".tflite")
    save_to_tflite(model, tflitepath)

    # save model info
    infopath = os.path.join(folder_name, name + ".info")

    if model_info == {}:
        model_info = create_model_info(model)
    with open(infopath, "w") as f:
        json.dump(model_info, f)


def save_to_tflite(model, model_path):
    """saves a model to its tflite equivalent.

    Args:
        model (Model): the model.
        model_path (string): the full path of where to save the model.
    """
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    open(model_path, "wb").write(tflite_model)


def create_model_info(model):
    """Generate the info dict from a model.

    Args:
        model (tf.keras.models.Model): the model.

    Returns:
        dict: the inputs / outputs info dict.

    """
    inputs = [
        [
            get_clean_layer_name(inp.name),
            inp.shape.as_list()[1:],
        ]
        for inp in model.inputs
    ]
    outputs = [
        [
            get_clean_layer_name(out.name),
            out.shape.as_list()[1:],
        ]
        for out in model.outputs
    ]
    return {"inputs": inputs, "outputs": outputs}


def load_model_info(model_path):
    """Load model info from file.

    Args:
        model_path (string): the full path of where the model is located.

    Raises:
        ValueError: raise an error if the path is invalid.

    Returns:
        dict: the inputs / outputs info dict.
    """
    if model_path.endswith(".tflite"):
        info_path = model_path.split(".tflite")[0] + ".info"
    elif model_path.endswith(".h5"):
        info_path = model_path.split(".h5")[0] + ".info"
    else:
        raise ValueError("Invalid model path")
    with open(info_path, "r") as f:
        return json.load(f)


def get_clean_layer_name(name):
    """Remove any unwanted characters from the layer name.

    Args:
        name (string): the layer name.

    Returns:
        string: the filtered layer name.
    """
    delimit_chars = ":_/"
    for char in delimit_chars:
        name = name.split(char)[0]
    return name


def predict_decorator(func, inputs, outputs):
    """Decorate the model.predict function.

    It used the __call__ of the model to avoid performance issues

    Args:
        func (method): the predict function
        inputs (list(tuple(string, list))): the inputs info list.
        outputs (list(tuple(string, list))): the outputs info list.

    Returns:
        method: the wrapped function.
    """
    if len(outputs) <= 1:

        def pred_to_dict(out):
            predictions = {}
            for (output_name, _) in outputs:
                predictions[output_name] = out[0][0]
            return predictions

    else:

        def pred_to_dict(out):
            predictions = {}
            for i, (output_name, _) in enumerate(outputs):
                value = out[i][0]
                if value.shape[0] == 1:
                    value = value[0]
                predictions[output_name] = value
            return predictions

    def wrapped_f(mem, *args, **kwargs):
        input_data = {}
        for input_name, _ in inputs:
            try:
                data = np.expand_dims(mem[input_name], 0).astype(np.float32)
                if len(data.shape) < 2:
                    data = np.expand_dims(data, 0)
                input_data[input_name] = data
            except KeyError:
                raise ValueError(f"input name {input_name} is not in memory")
        out = func(input_data, *args, **kwargs, training=False)
        return pred_to_dict(out)

    return wrapped_f


def freeze_conv(model):
    """Freeze all convolutional layers in a model.

    Args:
        model (tf.keras.models.Model): the model.
    """
    for layer in model.layers:
        if (
            isinstance(layer, tf.keras.layers.Conv2D)
            or isinstance(layer, tf.keras.layers.DepthwiseConv2D)
            or isinstance(layer, tf.keras.layers.SeparableConv2D)
        ):
            layer.trainable = False


class TFLiteModel:
    """Class to predict using a TFLite model."""

    def __init__(self, model_path, *args, **kwargs):
        """Init of the class.

        Args:
            model_path (string): full path of where the model is saved.
        """
        try:
            # try to load tflite runtime on raspberrypi
            import tflite_runtime.interpreter as tflite
        except ImportError:
            logging.info("failed to import tflite_runtime.interpreter, using tf.lite")
            import tensorflow.lite as tflite
        self.interpreter = tflite.Interpreter(
            model_path=model_path, num_threads=2, *args, **kwargs
        )

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.signatures = self.interpreter.get_signature_list()
        logging.info(f"Model signatures: {self.signatures}")

        self.runner = self.interpreter.get_signature_runner("serving_default")

    def predict(self, mem):
        """Get the model output from input_data.

        Args:
            input_data (list(np.array)): the input_data list. the length may vary between models

        Returns:
            dict: a dict containing all the predictions.
        """
        input_data = {}
        for input_name in self.signatures["serving_default"]["inputs"]:
            try:
                data = np.expand_dims(mem[input_name], 0).astype(np.float32)
                if len(data.shape) < 2:
                    data = np.expand_dims(data, 0)
                input_data[input_name] = data
            except KeyError:
                raise ValueError(f"input name {input_name} is not in memory")

        output_dict = self.runner(**input_data)
        predictions = {}

        for (output_name, output_data) in output_dict.items():
            if output_data.shape[1] == 1:
                output_data = output_data[0][0]
            else:
                output_data = output_data[0]
            predictions[output_name] = output_data

        return predictions
