import socketio
import uuid

uid = uuid.uuid4().hex

sio = socketio.Client()


@sio.on("connect")
def on_connect():
    print("connected")
    sio.emit("py-client-connected", uid)


@sio.on("disconnect")
def on_disconnect():
    print("disconnected")


@sio.on("test")
def on_message(data):
    print(data)
    sio.emit("logs", "LOG" + data)


sio.connect("ws://localhost:3000")
