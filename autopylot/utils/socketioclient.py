import time
from collections import deque
import uuid

import socketio
from . import memory, logger

mem = memory.mem
log_queue = deque(maxlen=100)

last_sent = time.time()
telemetry_delay = 0.03
do_send_telemetry = False
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
    global last_sent

    wait_for_connection(host)

    while not stop_thread:
        if not sio.connected and not stop_thread:
            wait_for_reconnection(host)

        for _ in range(len(log_queue)):
            send_log(log_queue[0])
            del log_queue[0]

        if do_send_telemetry:
            now = time.time()
            if mem.last_modified > last_sent and (now - last_sent) > telemetry_delay:
                send_telemetry(logger.serialize(mem))
                last_sent = now
            else:
                time.sleep(now - last_sent)

    sio.disconnect()
