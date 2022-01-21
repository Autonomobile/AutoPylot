"""Test the serial control."""
from ..controls import serial_control
from unittest import mock


def test_serial_control():
    test_memory = {}
    ser = serial_control.SerialControl(test_memory, port="loop")
    # ser.ser.readlines = mock.MagicMock(return_value=["1234"])
