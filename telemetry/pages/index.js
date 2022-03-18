import Head from "next/head";
import Image from "next/image";
import { useAtom } from "jotai";
import socketAtom from "../utils/client";
import memoryAtom from "../utils/memory";

export default function Home() {
  const [socket] = useAtom(socketAtom);
  const [memory] = useAtom(memoryAtom);

  const getImage = () => "data:image/jpeg;base64," + memory.image;

  function sendMessage() {
    const msg = document.getElementById("msg").value;
    socket.emit("py-test", msg);
  }

  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      {/* <button onClick={sendMessage}> Send Message </button> */}
      {/* <input id="msg" type="text" /> */}
    </>
  );
}
