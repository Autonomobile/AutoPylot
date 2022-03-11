import socketio
from collections import deque

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


def run_threaded(host):
    sio.connect(host)

    while True:
        if len(log_queue) != 0:
            log = log_queue.popleft()
            sio.emit("logs", log)
        if len(telemetry_queue) != 0:
            telemetry = telemetry_queue.popleft()
            sio.emit("telemetry", telemetry)
