"""Test the serial control."""
from ..controls import serial_control


def test_serial_high_speed():
    test_memory = {}

    # this should fail to open
    ser = serial_control.SerialControl(test_memory, port="test")

    # corresponds to high RPM
    ser.__decode_out__(b"1234\r\n")
    assert test_memory["speed"] == 11.57675387821255


def test_serial_normal_speed():
    test_memory = {}

    # this should fail to open
    ser = serial_control.SerialControl(test_memory, port="test")

    # corresponds to normal-ish RPM
    ser.__decode_out__(b"5678\r\n")
    assert test_memory["speed"] == 2.515976450460424


def test_serial_no_speed():
    test_memory = {}

    # this should fail to open
    ser = serial_control.SerialControl(test_memory, port="test")

    # out of bounds RPM value (considered as no speed)
    ser.__decode_out__(b"27001\r\n")
    assert test_memory["speed"] == 0
