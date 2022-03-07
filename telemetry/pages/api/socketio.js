import { Server } from 'socket.io'

// const 

const ioHandler = (req, res) => {
  if (!res.socket.server.io) {
    console.log('*First use, starting socket.io')

    const io = new Server(res.socket.server)

    io.on('connection', (socket) => {

      socket.broadcast.emit('ui-client-connected')

      socket.on('send-msg', (msg) => {
        // socket.broadcast.emit('receive-msg', msg)
        io.emit('receive-msg', msg)
      })

      socket.on("disconnect", () => {
        console.log("disconnect");
      });
    })

    res.socket.server.io = io
  } else {
    console.log('socket.io already running')
  }
  res.end()
}

export const config = {
  api: {
    bodyParser: false
  }
}

export default ioHandler