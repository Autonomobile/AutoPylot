import { atom } from "jotai";
import io from "socket.io-client";
import crypto from "crypto";

function getUuid() {
  if (typeof window !== "undefined") {
    const uuid = localStorage.getItem("uuid");
    
    if (uuid) {
      return uuid;
    }
    const newUUID = crypto.randomBytes(16).toString("hex");
    localStorage.setItem("uuid", newUUID);

    return newUUID;
  }
}

function getSocket() {
  const uiid = getUuid();

  const socket = io({
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000,
  });

  socket.on("connect", () => {
    socket.emit("ui-client-connected", uiid);
  });

  socket.on("reconnect", () => {
    socket.emit("ui-client-connected", uiid);
    console.log("reconnect");
  });

  const onError = (error) => socket.disconnect();
  socket.on("connect_failed", onError);
  socket.on("connect_error", onError);
  socket.on("connect_timeout", onError);
  socket.on("error", onError);

  socket.on("disconnect", () => {
    console.log("disconnect");
  });

  return socket;
}

export const socketAtom = atom(getSocket());

export const logsAtom = atom([]);

export const memoryAtom = atom({});

export const settingsAtom = atom({"please choose a car": ":)"});

export const carsAtom = atom([]);

export const carAtom = atom("");

export const notificationsAtom = atom([]);
