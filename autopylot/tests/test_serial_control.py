"""Test the serial control."""
from ..controls import serial_control
import time


def test_serial_high_speed():
    test_memory = {}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.start_thread()

    # corresponds to normal-ish RPM
    ser.ser.write(b"1234\r\n")

    # give some time for the decoding thread
    time.sleep(0.001)

    # stop the thread
    ser.stop()
    assert test_memory["speed"] == 11.57675387821255


def test_serial_normal_speed():
    test_memory = {}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.start_thread()

    # corresponds to normal-ish RPM
    ser.ser.write(b"5678\r\n")

    # give some time for the decoding thread
    time.sleep(0.001)

    # stop the thread
    ser.stop()

    assert test_memory["speed"] == 2.515976450460424


def test_serial_no_speed():
    test_memory = {}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.start_thread()
    ser.__throttle = 127

    ser.ser.write(b"27001\r\n")

    # give some time for the decoding thread
    time.sleep(0.001)

    # stop the thread
    ser.stop()

    assert test_memory["speed"] == 0.0


def test_serial_invalid_bitarray():
    test_memory = {}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.start_thread()

    ser.ser.write(b"1234")

    # give some time for the decoding thread
    time.sleep(0.001)

    # stop the thread
    ser.stop()
    assert test_memory.get("speed") is None


def test_serial_send_positive_steering():
    # simulate right turn
    test_memory = {"steering": 0.5}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.update()

    out = ser.ser.readlines()[-1]
    assert out == b"\xff\xbf\x7f\x00"


def test_serial_send_negative_steering():
    # simulate left turn
    test_memory = {"steering": -0.5}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.update()

    out = ser.ser.readlines()[-1]
    assert out == b"\xff?\x7f\x00"


def test_serial_send_positive_throttle():
    # simulate forward throttle
    test_memory = {"throttle": 0.5}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.update()

    out = ser.ser.readlines()[-1]
    assert out == b"\xff\x7f\xbf\x00"


def test_serial_send_negative_throttle():
    # simulate backward throttle
    test_memory = {"throttle": -0.5}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.update()

    out = ser.ser.readlines()[-1]
    assert out == b"\xff\x7f?\x00"


def test_serial_send_both():
    # simulate right turn and forward throttle
    test_memory = {"steering": 0.5, "throttle": 0.5}

    # open a test serial
    ser = serial_control.SerialControl(test_memory, port="loop://")
    ser.update()

    out = ser.ser.readlines()[-1]
    assert out == b"\xff\xbf\xbf\x00"
