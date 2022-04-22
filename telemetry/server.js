const logger = require("npmlog");
const app = require("express")();
const server = require("http").Server(app);
const io = require("socket.io")(server);
const qrcode = require("qrcode-terminal");
const network = require("./utils/network");

const config = require("./utils/config");
const dev = config["NODE_ENV"] !== "production";
const hostname = config["HOSTNAME"] || "0.0.0.0";
const port = config["PORT"] || 3000;
logger.level = config["LOG_LEVEL"] || "debug";

const next = require("next");
const nextapp = next({ dev, hostname, port });
const nextHandler = nextapp.getRequestHandler();
const ips = network.getLocalIpAdress();
const clients = {};


nextapp.prepare().then(() => {
  app.get("*", (req, res) => {
    return nextHandler(req, res);
  });

  server.listen(port, (err) => {
    if (err) throw err;
    for (const ip of ips) {
      logger.info("Server", `Ready on http://${ip}:${port}`);
      qrcode.generate(`http://${ip}:${port}`, { small: true });
    }
  });
});


io.on("connection", (socket) => {
  logger.info(`[SIO][--]`, `[${socket.id}] is connected`);

  socket.on("ui-client-connected", (uuid) => {
    logger.info(`[SIO][UI]`, `[${socket.id}][${uuid}] is authenticated`);
    clients[socket.id] = { socket: socket, uuid: uuid, type: "UI", car: "" };
    socket.join("UI");
    emitNotification("info", "Welcome to the dashboard", false);
  });

  socket.on("py-client-connected", (uuid) => {
    logger.info(`[SIO][PY]`, `[${socket.id}][${uuid}] is authenticated`);
    clients[socket.id] = {
      socket: socket,
      uuid: uuid,
      type: "PY",
      streamers: [],
    };
    socket.join("PY");
    updateCars();
    emitNotification("success", "A new car is available", true);
  });

  socket.on("disconnect", () => {
    if (clients[socket.id]) {
      const uuid = clients[socket.id].uuid;
      const type = clients[socket.id].type;
      delete clients[socket.id];

      logger.info(`[SIO][${type}]`, `[${socket.id}][${uuid}] is disconnected`);

      const ui_clients = getUiClients();

      if (type === "PY") {
        updateCars();
        for (const ui_client of ui_clients) {
          if (ui_client.car === socket.id) {
            ui_client.car = "";
          }
        }
        emitNotification("warning", `Car with ID [${socket.id}] is not available anymore`, true);
      } else if (type === "UI") {
        forgetUIClient(socket.id);
      }
    } else {
      logger.info(`[SIO][--]`, `[unknown] is disconnected`);
    }
  });

  socket.on("GET_CARS", () => {
    if (clients[socket.id]) {
      const uuid = clients[socket.id].uuid;
      logger.info(`[SIO][UI]`, `[${socket.id}][${uuid}] requested cars`);
    }
    else {
      logger.info(`[SIO][--]`, `[unknown] requested cars`);
    }
    const py_clients = getPyClients();
    socket.emit(
      "GET_CARS",
      py_clients.map((client) => client.socket.id)
    );
  });

  socket.on("SET_CAR", (py_client_id) => {
    if (clients[socket.id]) {
      const uuid = clients[socket.id].uuid;
      logger.info(
        `[SIO][UI]`,
        `[${socket.id}][${uuid}] choose [${py_client_id}] as main car`
      );
        
      console.log(py_client_id);

      forgetUIClient(socket.id); // tell this car to forget the UI client

      const ui_client = clients[socket.id];
      ui_client.car = py_client_id;

      if (py_client_id !== "") {
        const py_client = clients[py_client_id];
        py_client.streamers.push(socket.id);
      }
    }
  });

  socket.on("GET_MEMORY", (data) => {
    emitToStreamers("GET_MEMORY", data);
  });

  socket.on("GET_LOGS", (data) => {
    emitToStreamers("GET_LOGS", data);
  });

  function emitNotification(severity, message, everyone = false) {
    console.log(severity, message);
    if (everyone) {
      io.to("UI").emit("GET_NOTIFICATIONS", { severity, message });
    }
    else {
      socket.emit("GET_NOTIFICATIONS", { severity, message });
    }
  }

  function getPyClients() {
    return Object.values(clients).filter((c) => c.type === "PY");
  }
  
  function getUiClients() {
    return Object.values(clients).filter((c) => c.type === "UI");
  }
  
  function updateCars() {
    const py_clients = getPyClients();
    io.to("UI").emit(
      "GET_CARS",
      py_clients.map((c) => c.socket.id)
    );
  }
  
  function forgetUIClient(ui_client_id) {
    const py_clients = getPyClients();
    for (const py_client of py_clients) {
      if (py_client.streamers.includes(ui_client_id)) {
        py_client.streamers.splice(py_client.streamers.indexOf(ui_client_id), 1);
      }
    }
  }
  
  function emitToStreamers(event, data) {
    const py_client = clients[socket.id];
    for (const streamer of py_client.streamers) {
      socket.to(streamer).emit(event, data);
    }
  }  
});
