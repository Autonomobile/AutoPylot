import socketio
import requests

# standard Python
sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connected')
    sio.emit('py-client-connected')

@sio.on('disconnect')
def on_disconnect():
    print('disconnected')

@sio.on('receive-msg')
def on_message(data):
    print(data)


response = requests.get('http://localhost:3000/api/socket-io')
print(response.text)

sio.connect('ws://localhost:3000')
sio.wait()
