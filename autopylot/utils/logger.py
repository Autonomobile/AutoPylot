import base64
import json
import logging
import os
import socket
import sys
import threading
import time
from collections import deque

import cv2
import numpy as np

pathlogs = os.path.join(os.getcwd(), "logs/logs.log")


def init(name="", pathlogs=pathlogs, host="0.0.0.0", port=8080):
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
    fileHandler = logging.FileHandler(pathlogs, mode="w")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    # this is to display logs in the stdout
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)

    # this is to send records to the server
    telemetryHandler = TelemetryHandler(host, port)
    telemetryHandler.setLevel(logging.TELEMETRY)
    logger.addHandler(telemetryHandler)
    return logger


def compress_image(img, encode_params=[int(cv2.IMWRITE_JPEG_QUALITY), 50]):
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

    def __init__(self, host, port):
        logging.Handler.__init__(self)

        assert isinstance(host, str)
        assert isinstance(port, int)
        self.address = (host, port)

        self.host = host
        self.port = port
        self.address = (host, port)
        self.sock = None
        self.closeOnError = False
        self.retryTime = None

        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

        self.__logs_queue = deque(maxlen=100)
        self.__telemetry_queue = deque(maxlen=5)

        self.__thread = None
        self.__stop_thread = False
        self.start_thread()

    def makeSocket(self, timeout=1):
        """
        A factory method which allows subclasses to define the precise
        type of socket they want.
        """
        result = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result.settimeout(timeout)
        try:
            result.connect(self.address)
        except OSError:
            result.close()
            raise
        return result

    def createSocket(self, block=True):
        """
        Try to create a socket, using an exponential backoff with
        a max retry time. Thanks to Robert Olson for the original patch
        (SF #815911) which has been slightly refactored.
        """
        now = time.time()
        # Either retryTime is None, in which case this
        # is the first time back after a disconnect, or
        # we've waited long enough.
        if self.retryTime is None:
            attempt = True
        else:
            attempt = now >= self.retryTime
        if attempt:
            try:
                self.sock = self.makeSocket()
                self.retryTime = None  # next time, no delay before trying
            except OSError:
                # Creation failed, so set the retry time and return.
                if self.retryTime is None:
                    self.retryPeriod = self.retryStart
                else:
                    self.retryPeriod = self.retryPeriod * self.retryFactor
                    if self.retryPeriod > self.retryMax:
                        self.retryPeriod = self.retryMax
                self.retryTime = now + self.retryPeriod
                if block:
                    time.sleep(self.retryPeriod)

    def send(self, b):
        """
        Send bytes to the socket.

        This function allows for partial sends which can happen when the
        network is busy.
        """
        if self.sock:
            try:
                self.sock.sendall(b + b"\n")
                return True
            except OSError:  # pragma: no cover
                self.sock.close()
                self.sock = None  # so we can call createSocket next time
                return False
        return False

    def serialize(self, data):
        return json.dumps(data, cls=NumpyArrayEncoder).encode("utf-8")

    def handleError(self, record):
        """
        Handle an error during logging.

        An error has occurred during logging. Most likely cause -
        connection lost. Close the socket so that we can retry on the
        next event.
        """
        if self.closeOnError and self.sock:
            self.sock.close()
            self.sock = None  # try to reconnect next time
        else:
            logging.Handler.handleError(self, record)

    def emit(self, record):
        """Add a record to the queue."""
        record_dict = dict(record.__dict__)
        if isinstance(record_dict["msg"], str):
            self.__logs_queue.append(record_dict)
        else:
            self.__telemetry_queue.append(record_dict)

    def close(self):
        """
        Closes the socket.
        """
        self.acquire()
        try:
            sock = self.sock
            if sock:
                self.sock = None
                sock.close()
            logging.Handler.close(self)
        finally:
            self.release()

    def __run_threaded__(self):
        """
        Serialize the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """

        while True:
            if self.sock is None:
                self.createSocket()

            if len(self.__logs_queue) != 0 and self.sock:
                record = self.__logs_queue[0]
                s = self.serialize(record)
                if self.send(s):
                    del self.__logs_queue[0]

            if len(self.__telemetry_queue) != 0 and self.sock:
                record = self.__telemetry_queue[0]
                s = self.serialize(record)
                if self.send(s):
                    del self.__telemetry_queue[0]

            if self.__stop_thread:
                self.__stop_thread = False
                break

    def start_thread(self):
        """Start the thread that sends messages and telemetry to the server."""
        if not self.__thread:
            self.__thread = threading.Thread(target=self.__run_threaded__, daemon=True)
            self.__thread.start()
            logging.info("Started thread to send telemetry.")
        else:
            logging.warning("Thread already running.")

    def stop_thread(self):
        """Stop the thread that sends messages and telemetry to the server."""
        if self.__thread and self.__thread.is_alive():
            logging.info("Stopping thread.")
            self.__stop_thread = True
            self.__thread.join()
            self.close()
            logging.info("Stopped thread.")
        else:
            logging.warning("Thread is not running.")
