import time
import uuid
import os

import queue
import socketio
import psutil

from .utils import encode_image
from .memory import mem
from .settings import settings, restart_car

log_queue = queue.Queue()
stop_thread = False

sio = socketio.Client()
uuidhex = uuid.uuid4().hex

CPU_USAGE = 0

@sio.on("connect")
def on_connect():
    print("connected")
    sio.emit("py-client-connected", uuidhex)


@sio.on("disconnect")
def on_disconnect():
    print("disconnected")


@sio.on("SET_MEMORY")
def on_set_memory(data):
    mem.update(data)


@sio.on("GET_SETTINGS_ASK")
def on_get_settings():
    sio.emit("GET_SETTINGS_ANS", settings.__dict__)


@sio.on("SET_SETTINGS")
def on_set_settings(data):
    settings.update(data)
    settings.to_json()


@sio.on("RESTART")
def on_restart():
    restart_car()


@sio.on("STOP")
def on_stop():
    os._exit(0)


def wait_for_connection(host, sleep=1):
    """Wait for the connection to be established.

    Args:
        host (string): the host.
        sleep (int, optional): sleep time. Defaults to 1.
    """
    while not sio.connected and not stop_thread:
        try:
            sio.connect(host)
        except Exception:
            time.sleep(sleep)


def wait_for_reconnection(sleep=1):
    """Wait for the client to reconnect.

    Args:
        sleep (int, optional): sleep time. Defaults to 1.
    """
    while not sio.connected:
        time.sleep(sleep)


def send_log(log):
    """Send log message to the server.

    Args:
        log (any): the log to send.
    """
    sio.emit("GET_LOGS", log)


def send_telemetry(telemetry):
    """Send telemetry message to the server.

    Args:
        telemetry (any): the telemetry to send.
    """
    sio.emit("GET_MEMORY", telemetry)


def run_threaded(host):
    last_sent = time.time()
    wait_for_connection(host)

    while not stop_thread:
        if not sio.connected and not stop_thread:
            wait_for_reconnection()

        for _ in range(log_queue.qsize()):
            log = log_queue.get()
            send_log(log)

        if settings.DO_SEND_TELEMETRY:
            now = time.time()
            if (now - last_sent) > settings.TELEMETRY_DELAY:
                to_send = mem.copy()
                if "image" in to_send.keys():
                    to_send["image"] = encode_image(mem["image"])

                cpu_usage =  psutil.cpu_percent()
                to_send["cpu_usage"] = CPU_USAGE = cpu_usage if cpu_usage != 0 else CPU_USAGE

                to_send["ram_usage"] = psutil.virtual_memory().percent

                send_telemetry(to_send)
                last_sent = now
            else:
                time.sleep(max(settings.TELEMETRY_DELAY - (now - last_sent), 0))

    sio.disconnect()
