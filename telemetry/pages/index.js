import Head from "next/head";
import Image from "next/image";
import { useAtom } from "jotai";
import socketAtom from "../utils/client";
import memAtom from "../utils/memory";
import Skeleton from "@mui/material/Skeleton";

export default function Home() {
  const [socket] = useAtom(socketAtom);
  const [memory] = useAtom(memAtom);

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
      <button onClick={sendMessage}> Send Message </button>
      <input id="msg" type="text" />
      {memory.image ? (
        <Image src={getImage()} alt="live" layout="responsive" />
      ) : (
        <Skeleton variant="rectangular" width="100%" height="100%" />
      )}
    </>
  );
}
