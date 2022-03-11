import { atom } from "jotai";
import io from "socket.io-client";

export const socketAtom = atom(io());
