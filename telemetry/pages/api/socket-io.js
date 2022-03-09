import { Server } from "socket.io";

const clients = {};

const ioHandler = (req, res) => {
  if (!res.socket.server.io) {
    console.log("starting socket.io...");
    const io = new Server(res.socket.server);

    io.on("connection", (socket) => {
      // socket.broadcast.emit("new client connected");

      socket.on("ui-client-connected", () => {
        console.log(`${socket.id} UI-client is connected`);
        clients[socket.id] = { socket: socket, type: "UI", cars: [] };
      });

      socket.on("py-client-connected", () => {
        console.log(`${socket.id} PY-client is connected`);
        clients[socket.id] = { socket: socket, type: "PY" };
      });

      socket.on("disconnect", () => {
        if (clients[socket.id]) {
          let type = clients[socket.id].type;
          delete clients[socket.id];
          console.log(`${socket.id} ${type}-client is disconnected`);
        } else {
          console.log(`${socket.id} is disconnected`);
        }
      });

      socket.on("telemetry", (data) => {
        // socket.broadcast.emit('receive-msg', msg)
        io.emit("receive-msg", data);
      });
    });

    res.socket.server.io = io;
  }
  res.end("OK");
};

export const config = {
  api: {
    bodyParser: false,
  },
};

export default ioHandler;
