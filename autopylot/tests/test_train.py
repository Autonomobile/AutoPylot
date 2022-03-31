"""Test the the TrainerModel class."""
import os
import pytest
import numpy as np
import shutil

from ..models import train, utils
from ..utils import settings

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
