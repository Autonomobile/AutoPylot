import base64
import json
import logging
import os
import sys
import threading

import cv2
import numpy as np

from . import socketioclient

pathlogs = __file__ + r"/../../../logs/logs.log"


def init(name="", pathlogs=pathlogs, host="ws://localhost:3000"):
    logger = logging.getLogger(name)

    # if the logger already exists, just return it
    for hdlr in logger.handlers:
        if isinstance(hdlr, TelemetryHandler):
            return logger

    logger.handlers = []

    logging.TELEMETRY = logging.DEBUG - 5
    logging.addLevelName(logging.TELEMETRY, "TELEMETRY")

    logger.setLevel(logging.TELEMETRY)
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)s] [%(name)s] [%(module)s] %(message)s"
    )

    # this is to write in the logs/log file
    fileHandler = logging.FileHandler(os.path.join(os.getcwd(), pathlogs), mode="w")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    # this is to display logs in the stdout
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)

    # this is to send records to the server
    telemetryHandler = TelemetryHandler(host)
    telemetryHandler.setLevel(logging.TELEMETRY)
    logger.addHandler(telemetryHandler)
    return logger


def compress_image(img, encode_params=[int(cv2.IMWRITE_JPEG_QUALITY), 90]):
    _, encimg = cv2.imencode(".jpg", img, encode_params)
    return encimg


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            if len(obj.shape) == 3:  # we are dealing with an image
                return base64.b64encode(compress_image(obj)).decode("utf-8")
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class TelemetryHandler(logging.Handler):
    """
    A handler class which writes logging records, in json format, to
    a streaming socket. The socket is kept open across logging calls.
    If the peer resets it, an attempt is made to reconnect on the next call.
    """

    def __init__(self, host):
        logging.Handler.__init__(self)

        self.thread = threading.Thread(target=socketioclient.run_threaded, args=(host,))
        self.thread.start()

    def handleError(self, record):
        """
        Handle an error during logging.

        An error has occurred during logging. Most likely cause -
        connection lost. Close the socket so that we can retry on the
        next event.
        """
        logging.Handler.handleError(self, record)

    def serialize(self, data):
        return json.dumps(data, cls=NumpyArrayEncoder)

    def emit(self, record):
        """Add a record to the queue."""
        record_dict = dict(record.__dict__)
        if isinstance(record_dict["msg"], str):
            socketioclient.log_queue.append(self.serialize(record_dict))
        else:
            socketioclient.telemetry_queue.append(self.serialize(record_dict))

    def stop_thread(self):
        socketioclient.stop_thread = True
        self.thread.join()
        socketioclient.stop_thread = False

    def close(self):
        self.stop_thread()
        logging.Handler.close(self)
