"""Tests the utils functions."""
from ..utils import utils


def test_map_value():
    """The map of 0 belongs to [-1.0, 1.0] into [0, 255] should be 127.5."""
    assert utils.map_value(0.0, -1.0, 1.0, 0, 255) == 127.5


def test_map_value_lower_bounds():
    """The lower bound should be respected."""
    assert utils.map_value(-2.0, -1.0, 1.0, 0, 255) == 0.0


def test_map_value_upper_bounds():
    """The upper bound should be respected."""
    assert utils.map_value(2.0, -1.0, 1.0, 0, 255) == 255.0


def test_deadzone_in_deadzone():
    """It should return 0.0 as the value is in the deadzone."""
    assert utils.deadzone(0.05, 0.1, center=0.0) == 0.0


def test_deadzone_outside_deadzone():
    """It should return 0.1 as the value is not in the deadzone."""
    assert utils.deadzone(0.1, 0.05, center=0.0) == 0.1


def test_deadzone_outside_deadzone_offcenter():
    """It should return 0.1 as the value is not in the deadzone."""
    assert utils.deadzone(0.1, 0.05, center=1.0) == 0.1


def test_deadzone_in_deadzone_offcenter():
    """It should return 1.0 as the value is in the deadzone."""
    assert utils.deadzone(1.05, 0.1, center=1.0) == 1.0
