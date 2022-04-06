"""Test the DataGenerator class."""
from ..datasets import datagenerator


def test_init():
    """Test the init of the DataGenerator class."""
    dataGenerator = datagenerator.DataGenerator(
        ["dummy_path.json"],
        inputs=["image", "speed"],
        outputs=["steering", "throttle"],
        batch_size=64,
    )
    assert dataGenerator.dimensions == 0
    assert dataGenerator.batch_size == 64
    assert dataGenerator.inputs == ["image", "speed"]
    assert dataGenerator.outputs == ["steering", "throttle"]


def test_call():
    """Test the call of the DataGenerator class."""
    dataGenerator = datagenerator.DataGenerator(
        ["dummy_path.json"],
        inputs=["image", "speed"],
        outputs=["steering", "throttle"],
        batch_size=64,
    )
    Xs, Ys = dataGenerator()
    assert Xs[0].shape == (64, 120, 160, 3)  # the image input
    assert Xs[1].shape == (64, 1, 1)  # the speed input

    assert Ys[0].shape == (64, 1, 1)  # the steering output
    assert Ys[1].shape == (64, 1, 1)  # the throttle output
