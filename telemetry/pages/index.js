import Head from "next/head";
import { useEffect } from "react";
import { useAtom } from "jotai";
import { socketAtom } from "../utils/client";

export default function Home() {
  const [socket, setSocket] = useAtom(socketAtom);

  useEffect(() => {
    socket.on("receive-msg", (data) => {
      console.log("data", data);
    });
  }, [socket, setSocket]);

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
