import { atom } from "jotai";
import io from "socket.io-client";
import crypto from "crypto";

function getSocket() {
  const uiid = getUiid();
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

function getUiid() {
  if (typeof window !== "undefined") {
    const uiid = localStorage.getItem("uiid");
    if (uiid) return uiid;
    const newUiid = crypto.randomBytes(16).toString("hex");
    localStorage.setItem("uiid", newUiid);
    return newUiid;
  }
}

const socketAtom = atom(getSocket());

export default socketAtom;
