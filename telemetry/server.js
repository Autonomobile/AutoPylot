const logger = require("npmlog");
const app = require("express")();
const server = require("http").Server(app);
const io = require("socket.io")(server);
const qrcode = require('qrcode-terminal');
const network = require("./utils/network");

const config = require("./utils/config");
const dev = config["NODE_ENV"] !== "production";
const hostname = config["HOSTNAME"] || "0.0.0.0";
const port = config["PORT"] || 3000;
logger.level = config["LOG_LEVEL"] || "debug";

const next = require("next");
const nextapp = next({ dev, hostname, port });
const nextHandler = nextapp.getRequestHandler();

const clients = {};

const ip = network.getLocalIpAdress();

nextapp.prepare().then(() => {
  app.get("*", (req, res) => {
    return nextHandler(req, res);
  });

  server.listen(port, (err) => {
    if (err) throw err;
    logger.info("Server", `Ready on http://${ip}:${port}`);
    qrcode.generate(`http://${ip}:${port}`, { small: true });
  });
});

io.on("connection", (socket) => {
  socket.broadcast.emit("new client connected");

  socket.on("ui-client-connected", (uuid) => {
    logger.info(
      `[socket.io][UI]`,
      `[${uuid}][${socket.id}] is connected`
    );
    clients[socket.id] = { socket: socket, uuid: uuid, type: "UI", cars: [] };
  });

  socket.on("py-client-connected", (uuid) => {
    logger.info(
      `[socket.io][PY]`,
      `[${uuid}][${socket.id}] is connected`
    );
    clients[socket.id] = { socket: socket, uuid: uuid, type: "PY", cars: [] };
  });

  socket.on("disconnect", () => {
    if (clients[socket.id]) {
      const uuid = clients[socket.id].uuid;
      const type = clients[socket.id].type;
      delete clients[socket.id];
      logger.info(`[socket.io][${type}]`, `[${uuid}][${socket.id}] is disconnected`);
    } else {
      logger.info(`[socket.io][--]`, `[unknown] is disconnected`);
    }
  });

  socket.on("telemetry", (data) => {
    socket.broadcast.emit("receive-telemetry", data);
  });

  socket.on("logs", (data) => {
    socket.broadcast.emit("receive-logs", data);
  });

  socket.on("py-test", (data) => {
    socket.broadcast.emit("test", data);
  });
});