import Head from "next/head";
import Image from "next/image";
import io from "socket.io-client";
import { useEffect, useState } from "react";
import { useAtom } from "jotai";
import { socketAtom } from "../utils/store";

export default function Home() {
  const [socket] = useAtom(socketAtom);

  useEffect(() => {
    const onError = (error) => {
      socket.disconnect();
    };
    socket.on("connect", () => {
      console.log("connect");
      console.log(socket);
      socket.emit("ui-client-connected");
    });
    socket.on("receive-msg", (data) => {
      console.log("data", data);
    });
    socket.on("connect_failed", onError);
    socket.on("connect_error", onError);
    socket.on("connect_timeout", onError);
    socket.on("error", onError);
    socket.on("disconnect", () => {
      console.log("disconnect");
    });
  }, [socket]);

  function sendMessage() {
    socket.emit("telemetry", "hello");
  }

  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      <button onClick={sendMessage}>Send Message</button>
    </>
  );
}
