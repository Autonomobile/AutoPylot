import json
import logging
import os

import tensorflow as tf
from tensorflow.keras.models import Model

from ..utils import settings

settings = settings.settings


def load_model(model_path, *args, **kwargs):
    """Load a model.

    Args:
        model_path (_type_): model_path relative to the settings.MODELS_PATH.

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
            model.predict = predict_decorator(model, model_info["outputs"])
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
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS,
    ]
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
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


def predict_decorator(func, outputs):
    """Decorate the model.predict function.

    It used the __call__ of the model to avoid performance issues

    Args:
        func (method): the predict function
        outputs (list(tuple(string, list))): the outputs info list.

    Returns:
        method: the wrapped function.
    """
    if len(outputs) <= 1:

        def pred_to_dict(out):
            predictions = {}
            for (name, _) in outputs:
                predictions[name] = out[0][0]
            return predictions

    else:

        def pred_to_dict(out):
            predictions = {}
            for i, (name, _) in enumerate(outputs):
                predictions[name] = out[i][0][0]
            return predictions

    def wrapped_f(*args, **kwargs):
        out = func(*args, **kwargs, training=False)
        return pred_to_dict(out)

    return wrapped_f


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
        self.interpreter = tflite.Interpreter(model_path=model_path, *args, **kwargs)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # load model info
        self.outputs = load_model_info(model_path)["outputs"]

    def predict(self, input_data):
        """Get the model output from input_data.

        Args:
            input_data (list(np.array)): the input_data list. the length may vary between models

        Returns:
            dict: a dict containing all the predictions.
        """
        for i, inp in enumerate(input_data):
            self.interpreter.set_tensor(self.input_details[i]["index"], inp)
        self.interpreter.invoke()

        output_dict = {}
        for ((name, shape), tensor) in zip(self.outputs, self.output_details):
            # single value
            if shape[0] == 1:
                output_dict[name] = self.interpreter.get_tensor(tensor["index"])[0][0]
            # array of neurons
            else:
                output_dict[name] = self.interpreter.get_tensor(tensor["index"])[0]

        return output_dict
