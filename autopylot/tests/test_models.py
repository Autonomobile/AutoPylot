import os
import shutil

import pytest
from autopylot.cameras import Camera
from autopylot.datasets import preparedata
from autopylot.models import architectures, utils
from autopylot.utils import memory, settings

dirpath = os.path.join(settings.settings.MODELS_PATH, "test", "test")


@pytest.mark.models
def test_create_model_save():
    model = architectures.test_model(
        [
            # testing with "list" shape
            ("steering", [1, 1]),
            # testing with "tuple" shape
            ("test_output", (1, 20)),
        ]
    )
    model.summary()
    utils.save(model, "test")

    assert (
        os.path.exists(dirpath + ".h5")
        and os.path.exists(dirpath + ".tflite")
        and os.path.exists(dirpath + ".info")
    )


@pytest.mark.models
def test_input_shapes():
    model, model_info = utils.load_model("test/test.tflite")

    for input_detail, (_, shape) in zip(model.input_details, model_info["inputs"]):
        assert tuple(input_detail["shape"][1:]) == tuple(shape)

    for output_detail, (_, shape) in zip(model.output_details, model_info["outputs"]):
        assert tuple(output_detail["shape"][1:]) == tuple(shape)


@pytest.mark.models
def test_expected_error():
    model, model_info = utils.load_model("test/test.tflite")
    prepare_data = preparedata.PrepareData(model_info)

    with pytest.raises(ValueError):
        prepare_data(memory.mem)


@pytest.mark.models
def test_tflite_predict():
    model, model_info = utils.load_model("test/test.tflite")
    prepare_data = preparedata.PrepareData(model_info)
    camera = Camera(camera_type="dummy")

    camera.update()
    memory.mem["speed"] = 0.123

    input_data = prepare_data(memory.mem)
    predictions = model.predict(input_data)
    assert predictions != {}


@pytest.mark.models
def test_tf_predict():
    model, model_info = utils.load_model("test/test.h5")
    prepare_data = preparedata.PrepareData(model_info)
    camera = Camera(camera_type="dummy")

    camera.update()
    memory.mem["speed"] = 2.3

    input_data = prepare_data(memory.mem)
    predictions = model.predict(input_data)
    assert predictions != {}


@pytest.mark.models
def test_delete_directory():
    """Deletes the created models."""
    shutil.rmtree(os.path.join(settings.settings.MODELS_PATH, "test"))
    assert os.path.exists(dirpath) is False
