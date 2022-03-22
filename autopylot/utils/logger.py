import base64
import logging
import os
import sys
import threading

import cv2

from . import settings, socketioclient

settings = settings.settings

pathlogs = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "logs/logs.log",
)


class SocketIOHandler(logging.Handler):
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

    def emit(self, record):
        """Add a record to the queue."""
        socketioclient.log_queue.put(dict(record.__dict__))

    def start_thread(self):
        self.thread.start()

    def stop_thread(self):
        socketioclient.stop_thread = True
        self.thread.join()
        socketioclient.stop_thread = False

    def close(self):
        self.stop_thread()
        logging.Handler.close(self)


def has_dtype(dtype, iterable):
    for item in iterable:
        if isinstance(item, dtype):
            return True


def has_dtypes(dtypes, iterable):
    for dtype in dtypes:
        if not has_dtype(dtype, iterable):
            return False
    return True


def init(
    name="",
    pathlogs=pathlogs,
    host=settings.SERVER_ADDRESS,
    handlers=[logging.FileHandler, logging.StreamHandler, SocketIOHandler],
    DO_SEND_TELEMETRY=False,
):
    logger = logging.getLogger(name)

    # if the logger already exists, just return it
    if has_dtypes(handlers, logger.handlers):
        return logger

    logger.handlers = []

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)s] [%(name)s] [%(module)s] %(message)s"
    )

    if settings.LOG_LEVEL == "debug":
        level = logging.DEBUG
    else:
        level = logging.INFO

    # this is to write in the logs/log file
    fileHandler = logging.FileHandler(pathlogs, mode="w")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(level)
    logger.addHandler(fileHandler)

    # this is to display logs in the stdout
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(level)
    logger.addHandler(streamHandler)

    # this is to send records to the server
    socketIOHandler = SocketIOHandler(host)
    socketIOHandler.setLevel(level)
    logger.addHandler(socketIOHandler)
    return logger
