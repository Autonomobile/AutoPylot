const app = require("express")();
const server = require("http").Server(app);
const io = require("socket.io")(server);

const dev = process.env.NODE_ENV !== "production";
const hostname = "localhost";
const port = 3000;

const next = require("next");
const nextapp = next({ dev, hostname, port });
const nextHandler = nextapp.getRequestHandler();

const clients = {};


nextapp.prepare().then(() => {
  app.get("*", (req, res) => {
    return nextHandler(req, res);
  });

  server.listen(port, (err) => {
    if (err) throw err;
    console.log(`> Ready on http://localhost:${port}`);
  });
});

io.on("connection", (socket) => {
  socket.broadcast.emit("new client connected");

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
    console.log(`${socket.id} telemetry: ${data}`);
    io.emit("receive-msg", data);
  });
});


// TODO: check if id exists