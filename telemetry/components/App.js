import { useState, useEffect } from "react";
import Head from "next/head";
import { useAtom } from "jotai";
import { IconButton, Drawer } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SideBar from "../components/SideBar";
import memoryAtom from "../utils/memory";
import socketAtom from "../utils/client";

export default function App({ children }) {
  const [drawerState, setDrawerState] = useState(false);
  const [socket] = useAtom(socketAtom);
  const [memory, setMemory] = useAtom(memoryAtom);

  const toggleDrawer = (open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    )
      return;
    setDrawerState(open);
  };

  useEffect(() => {
    socket.off("receive-telemetry"); // remove old listener
    socket.on("receive-telemetry", (data) => {
      setMemory(data);
      console.log("memory app", data);
    });
    socket.off("receive-logs"); // remove old listener
    socket.on("receive-logs", (data) => {
      console.log(data);
    });
    const appHeight = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`);
    };
    window.addEventListener("resize", appHeight);
    appHeight();
  }, [socket, setMemory, memory]);

  return (
    <>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="viewport"
          content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width, height=device-height, target-densitydpi=device-dpi"
        />
      </Head>
      <div className="flex flex-col screen-height overflow-auto">
        <Drawer anchor="left" open={drawerState} onClose={toggleDrawer(false)}>
          <SideBar closeDrawer={() => setDrawerState(false)} />
        </Drawer>
        <div className="flex h-16 bg-blue-500 google-shadow z-10">
          <div className="h-full w-16 block md:hidden bg-inherit">
            <div className="flex h-full">
              <div className="m-auto">
                <IconButton onClick={toggleDrawer(true)}>
                  <MenuIcon className="text-white" />
                </IconButton>
              </div>
            </div>
          </div>
          <div className="flex flex-1 h-full">
            <div className="my-auto ml-0 md:ml-8">
              <h1 className="google-font text-xl font-normal text-white select-none">
                Telemetry Server
              </h1>
            </div>
          </div>
        </div>
        <div className="flex flex-1 min-h-0">
          <div className="flex-none w-60 hidden md:block">
            <SideBar />
          </div>
          <div className="flex flex-col flex-1 bg-gray-100">
            <div className="flex-1 overflow-y-auto">{children}</div>
          </div>
        </div>
      </div>
    </>
  );
};