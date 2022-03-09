import Head from "next/head";
import Image from "next/image";
import io from "socket.io-client";
import { useEffect, useState } from "react";
import { useAtom } from "jotai";
import { socketAtom } from "../utils/store";
import { Dash } from "../components/Dash";
import { Dashboard } from "../components/Dashboard";


export default function Home() {
  // const [socket, setSocket] = useAtom(socketAtom);

  const onError = (error) => {
    console.log(error);
  };

  useEffect(() => {
    // fetch("/api/socket-io")
    //   .then(() => {
    //     const client = io();
    //     setSocket(client);
    //     client.on("connect", () => {
    //       console.log("connect");
    //       console.log(client);
    //       client.emit("ui-client-connected");
    //     });
    //     client.on("receive-msg", (data) => {
    //       console.log("data", data);
    //     });
    //     socket.on("connect_failed", onError);
    //     socket.on("connect_error", onError);
    //     socket.on("connect_timeout", onError);
    //     socket.on("error", onError);
    //     client.on("disconnect", () => {
    //       console.log("disconnect");
    //     });
    //   })
    //   .catch((err) => {
    //     console.log(err);
    //   });
  }, []);

  return (
    <Dashboard/>
    // <Dash/>
  );
}
