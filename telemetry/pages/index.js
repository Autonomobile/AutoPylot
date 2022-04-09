import { useEffect, useState } from "react";
import Head from "next/head";
import { useAtom } from "jotai";
import { socketAtom, carsAtom, carAtom } from "../utils/atoms";

export default function Home() {
  const [socket] = useAtom(socketAtom);

  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      <div id="terminal" className="h-full w-full bg-black p-10 max-w-full">
        hello world
      </div>
    </>
  );
}
