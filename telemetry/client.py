import socketio

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

sio.connect('ws://localhost:3000')
