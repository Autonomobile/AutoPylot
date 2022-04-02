from email.mime import image
import json
import socketio
import uuid

uid = uuid.uuid4().hex
sio = socketio.Client()


@sio.on("connect")
def on_connect():
    print("connected")
    sio.emit("py-client-connected", uid)
    while True:
        black_base64_img = "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
        gray_base64_img = "R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="
        sio.emit("logs", input(">> "))
        sio.emit("telemetry", {"image": black_base64_img})
        sio.emit("logs", input(">> "))
        sio.emit("telemetry", {"image": gray_base64_img})


@sio.on("disconnect")
def on_disconnect():
    print("disconnected")


@sio.on("test")
def on_message(data):
    print(data)
    sio.emit("logs", "LOG" + data)


sio.connect("ws://localhost:3000")
