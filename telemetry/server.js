//@ts-check
const logger = require("npmlog");
const app = require("express")();
// @ts-ignore
const server = require("http").Server(app);
// @ts-ignore
const io = require("socket.io")(server);
const qrcode = require("qrcode-terminal");
const network = require("./utils/network");

const config = require("./utils/config");
const dev = config["NODE_ENV"] !== "production";
const hostname = config["HOSTNAME"] || "0.0.0.0";
const port = config["PORT"] || 3000;
logger.level = config["LOG_LEVEL"] || "debug";

const next = require("next");
// @ts-ignore
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

  // TODO: add doc + better params name
  socket.on("ui-client-connected", (uuid) => {
    logger.info(`[SIO][UI]`, `[${socket.id}][${uuid}] is authenticated`);
    clients[socket.id] = { socket: socket, uuid: uuid, type: "UI", car: "" };
    socket.join("UI");
    const py_clients = getPyClients();
    emitNotification(
      "info",
      `Welcome to the dashboard. You can now take the control of ${py_clients.length} available cars.`,
      false
    );
  });

  // TODO: add doc + better params name
  socket.on("py-client-connected", (uuid) => {
    logger.info(`[SIO][PY]`, `[${socket.id}][${uuid}] is authenticated`);
    clients[socket.id] = {
      socket: socket,
      uuid: uuid,
      type: "PY",
    };
    socket.join("PY");
    updateCars();
    emitNotification("success", "A new car is available", true);
  });

  // client to server
  // TODO: add doc + better params name
  socket.on("disconnect", () => {
    if (clients[socket.id]) {
      const uuid = clients[socket.id].uuid;
      const type = clients[socket.id].type;
      delete clients[socket.id];

      logger.info(`[SIO][${type}]`, `[${socket.id}][${uuid}] is disconnected`);

      if (type === "PY") {
        io.to(`PY_${socket.id}`).socketsLeave(`PY_${socket.id}`);
        updateCars();
        emitNotification(
          "warning",
          `Car with ID [${socket.id}] is not available anymore`,
          true
        );
      }
    } else {
      logger.info(`[SIO][--]`, `[unknown] is disconnected`);
    }
  });

  // ui to server
  // TODO: add doc + better params name
  socket.on("GET_CARS", () => {
    if (clients[socket.id]) {
      const uuid = clients[socket.id].uuid;
      logger.info(`[SIO][UI]`, `[${socket.id}][${uuid}] requested cars`);
    } else {
      logger.info(`[SIO][--]`, `[unknown] requested cars`);
    }
    const py_clients = getPyClients();
    const cars = py_clients.map((client) => client.socket.id);
    socket.emit("GET_CARS", cars);
  });

  // ui to server
  // TODO: add doc + better params name
  socket.on("SET_CAR", (new_car) => {
    const ui_client = clients[socket.id];
    if (ui_client) {
      const uuid = clients[socket.id].uuid;
      logger.info(
        `[SIO][UI]`,
        `[${socket.id}][${uuid}] choose [${new_car}] as main car`
      );

      socket.leave(`PY_${ui_client.car}`);
      if (new_car !== "") {
        ui_client.car = new_car;
        socket.join(`PY_${ui_client.car}`);
      }
    }
  });

  // py to ui
  // TODO: add doc + better params name
  socket.on("GET_MEMORY", (data) => {
    socket.to(`PY_${socket.id}`).emit("GET_MEMORY", data);
  });

  // py to ui
  // TODO: add doc + better params name
  socket.on("GET_LOGS", (data) => {
    socket.to(`PY_${socket.id}`).emit("GET_LOGS", data);
  });

  // ui to py
  // TODO: add doc + better params name
  socket.on("GET_SETTINGS", (car_id) => {
    if (car_id !== "") {
      socket.join(`PY_${car_id}_SETTINGS`);
      socket.to(car_id).emit("GET_SETTINGS_ASK");
    }
  });

  // py to ui
  // TODO: add doc + better params name + async
  socket.on("GET_SETTINGS_ANS", async (data) => {
    const room = `PY_${socket.id}_SETTINGS`;
    socket.to(room).emit("GET_SETTINGS", data);
    io.to(room).socketsLeave(room);
  });

  // TODO: add doc + better params name
  socket.on("SET_SETTINGS", (settings) => {
    const car = clients[socket.id].car;
    socket.to(car).emit("SET_SETTINGS", settings);
    emitNotification("success", `Settings updated for ${car}`, true);
  });


  // TODO: add doc + better params name
  socket.on("RESTART", (car_id) => {
    const car = clients[socket.id].car;
    socket.to(car).emit("RESTART");
    emitNotification("success", `Restarting ${car}`, true);
  });

  // TODO: add doc + better params name
  socket.on("STOP", (car_id) => {
    const car = clients[socket.id].car;
    socket.to(car).emit("STOP");
    emitNotification("success", `Stoping ${car}`, true);
  });


  // TODO: add doc
  function emitNotification(severity, message, everyone = false) {
    if (everyone) {
      io.to("UI").emit("GET_NOTIFICATIONS", { severity, message });
    } else {
      socket.emit("GET_NOTIFICATIONS", { severity, message });
    }
  }

  function getPyClients() {
    return Object.values(clients).filter((c) => c.type === "PY");
  }

  // TODO: remove this function
  function getUiClients() {
    return Object.values(clients).filter((c) => c.type === "UI");
  }

  // TODO: add doc
  function updateCars() {
    const py_clients = getPyClients();
    const cars = py_clients.map((client) => client.socket.id);
    io.to("UI").emit("GET_CARS", cars);
  }

});
