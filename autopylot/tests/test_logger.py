import logging

import numpy as np

from ..utils import logger, utils, settings

settings = settings.settings


def test_init_root():
    log = logger.init()
    assert log.name == "root"
    assert len(log.handlers) == 3

    assert isinstance(log.handlers[0], logging.FileHandler)
    assert isinstance(log.handlers[1], logging.StreamHandler)
    assert isinstance(log.handlers[2], logger.SocketIOHandler)


def test_file_logs():
    logging.info("test logging to file !")

    with open(settings.LOGS_PATH, "r") as f:
        lines = f.readlines()

    assert lines[-1].endswith("test logging to file !\n")


def test_stop_thread():
    log = logger.init()
    assert isinstance(log.handlers[2], logger.SocketIOHandler)
    log.handlers[2].stop_thread()
