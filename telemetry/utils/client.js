import { atom } from "jotai";
import io from "socket.io-client";

export function getSocket() {
  const socket = io();
  socket.on("connect", () => {
    socket.emit("ui-client-connected");
  });
  const onError = (error) => {
    socket.disconnect();
  };
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
