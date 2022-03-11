import Head from "next/head";
import { useEffect } from "react";
import { useAtom } from "jotai";
import { socketAtom } from "../utils/client";


export default function Home() {
  const [socket, setSocket] = useAtom(socketAtom);

  useEffect(() => {
    socket.off("receive-logs");
    socket.on("receive-logs", (data) => {
      console.log("logs", data);
    });
    socket.off("receive-telemetry");
    socket.on("receive-telemetry", (data) => {
      console.log("telemetry", data);
    });
  }, [socket, setSocket]);

  function sendMessage() {
    const msg = document.getElementById("msg").value;
    socket.emit("py-test", msg);
  }

  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      <button onClick={sendMessage}>Send Message</button>
      <input id="msg" type="text" />
    </>
  );
}
