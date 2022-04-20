"""Test the the TrainerModel class."""
import os
import shutil
import time

import numpy as np
import pytest

from ..models import train, utils
from ..utils import io, settings

settings = settings.settings


@pytest.mark.models
def test_model_creation():
    """Test model creation and saving."""
    trainer = train.TrainModel(name="test_model_creation", try_load=False)
    assert trainer.model is not None
    assert trainer.model_info is not None
    assert trainer.name == "test_model_creation"


@pytest.mark.models
def test_model_try_load():
    """Test that the model is created and not loaded."""
    trainer = train.TrainModel(name="test_model_try_load", try_load=True)
    assert trainer.model is not None
    assert trainer.model_info is not None
    assert trainer.name == "test_model_try_load"

    with pytest.raises(ValueError):
        utils.load_model(
            os.path.join(
                settings.MODELS_PATH, "test_model_try_load", "test_model_try_load.h5"
            )
        )


@pytest.mark.models
def test_model_successfull_load():
    """Test that the model is loaded from file successfully."""
    trainer = train.TrainModel(name="test_model_successfull_load", try_load=False)
    assert trainer.model is not None
    assert trainer.model_info is not None
    assert trainer.name == "test_model_successfull_load"

    utils.save_model(trainer.model, trainer.name)
    model_path = os.path.join(settings.MODELS_PATH, trainer.name, trainer.name)
    assert (
        os.path.exists(model_path + ".h5")
        and os.path.exists(model_path + ".tflite")
        and os.path.exists(model_path + ".info")
    )

    loaded_model, loaded_info = utils.load_model(model_path + ".h5")
    assert loaded_model is not None
    assert loaded_info is not None
    for w1, w2 in zip(trainer.model.get_weights(), loaded_model.get_weights()):
        assert np.array_equal(w1, w2)

    shutil.rmtree(os.path.join(settings.MODELS_PATH, trainer.name))


@pytest.mark.models
def test_model_training():
    """Save dummy dataset to file and trains the model."""
    trainer = train.TrainModel(name="test_model_training", try_load=False)
    assert trainer.model is not None
    assert trainer.model_info is not None
    assert trainer.name == "test_model_training"

    dataset_path = os.path.join(settings.DATASET_PATH, "test_model_training")
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)

    for _ in range(100):
        image_data = {
            "image": np.zeros((120, 160, 3), dtype=np.uint8),
            "speed": np.random.random() * 5,
            "steering": (np.random.random() - 0.5) * 2,
            "throttle": np.random.random(),
        }
        assert io.save_image_data(
            image_data,
            os.path.join(
                dataset_path,
                settings.JSON_FILE_FORMAT.format(t=time.time()),
            ),
        ) == (True, True)

    trainer.train(dataset_path, batch_size=8, epochs=1)
    shutil.rmtree(dataset_path)
    shutil.rmtree(os.path.join(settings.MODELS_PATH, "test_model_training"))
