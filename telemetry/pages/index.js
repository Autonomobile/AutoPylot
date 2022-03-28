import { useEffect, useState } from "react";
import Head from "next/head";
import { useAtom } from "jotai";
import { socketAtom, carsAtom, carAtom } from "../utils/atoms";

export default function Home() {
  const [socket] = useAtom(socketAtom);

  function getCars() {
    // socket.emit("test");
  }

  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      <button onClick={getCars}>Get Cars</button>
    </>
  );
}
