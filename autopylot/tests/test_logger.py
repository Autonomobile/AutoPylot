import logging
import os

import numpy as np

from ..utils import logger


def test_init_root():
    log = logger.init()
    assert log.name == "root"
    assert len(log.handlers) == 3

    assert isinstance(log.handlers[0], logging.FileHandler)
    assert isinstance(log.handlers[1], logging.StreamHandler)
    assert isinstance(log.handlers[2], logger.TelemetryHandler)


def test_compress_image():
    img = np.zeros((120, 160, 3))
    compressed = logger.compress_image(img)

    assert compressed.shape[0] == 947


def test_serialize_json():
    log = logger.init()
    mem = {"msg": {"image": np.zeros((120, 160, 3))}}

    assert isinstance(log.handlers[2], logger.TelemetryHandler)
    serialized = log.handlers[2].serialize(mem)

    assert isinstance(serialized, bytes) and len(serialized) == 1286


def test_file_logs():
    logging.info("test logging to file !")

    with open(logger.pathlogs, "r") as f:
        lines = f.readlines()

    assert lines[-1].endswith("test logging to file !\n")


def test_stop_thread():
    log = logger.init()
    assert isinstance(log.handlers[2], logger.TelemetryHandler)
    log.handlers[2].stop_thread()
