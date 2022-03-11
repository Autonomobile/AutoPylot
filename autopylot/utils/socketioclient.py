import time
from collections import deque

import socketio

log_queue = deque(maxlen=100)
telemetry_queue = deque(maxlen=5)
stop_thread = False

sio = socketio.Client()


@sio.on("connect")
def on_connect():
    print("connected")
    sio.emit("py-client-connected")


@sio.on("disconnect")
def on_disconnect():
    print("disconnected")


@sio.on("receive-msg")
def on_message(data):
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
            wait_for_connection(host)

        for _ in range(len(log_queue)):
            send_log(log_queue[0])
            del log_queue[0]

        for _ in range(len(telemetry_queue)):
            send_telemetry(telemetry_queue[0])
            del telemetry_queue[0]
