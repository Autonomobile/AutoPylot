import time
from collections import deque
import uuid

import socketio
from . import memory, logger

mem = memory.mem
log_queue = deque(maxlen=100)
stop_thread = False

sio = socketio.Client()
uuidhex = uuid.uuid4().hex


@sio.on("connect")
def on_connect():
    print("connected")
    sio.emit("py-client-connected", uuidhex)


@sio.on("disconnect")
def on_disconnect():
    print("disconnected")


@sio.on("test")
def on_test(data):
    print(data)


def wait_for_connection(host, sleep=1):
    while not sio.connected and not stop_thread:
        try:
            sio.connect(host)
        except Exception:
            time.sleep(sleep)


def wait_for_reconnection(sleep=1):
    while not sio.connected:
        time.sleep(sleep)


def send_log(log):
    sio.emit("logs", log)


def send_telemetry(telemetry):
    sio.emit("telemetry", telemetry)


def run_threaded(host):
    wait_for_connection(host)

    while not stop_thread:
        if not sio.connected:
            wait_for_reconnection(host)

        for _ in range(len(log_queue)):
            send_log(log_queue[0])
            del log_queue[0]

        if "image" in mem.keys():
            send_telemetry(logger.serialize(mem))
        else:
            time.sleep(1)

    sio.disconnect()
