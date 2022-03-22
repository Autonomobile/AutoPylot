import { useState, useEffect } from "react";
import Head from "next/head";
import { useAtom } from "jotai";
import { socketAtom, memoryAtom, logsAtom, settingsAtom } from "../utils/atoms";
import { IconButton, Drawer } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SideBar from "../components/SideBar";
import DropDown from "../components/DropDown";

export default function App({ children }) {
  const [drawerState, setDrawerState] = useState(false);
  const [socket] = useAtom(socketAtom);
  const [, setMemory] = useAtom(memoryAtom);
  const [, setLogs] = useAtom(logsAtom);
  const [, setSettings] = useAtom(settingsAtom);
  // const [, setNotification] = useAtom(notificationsAtom);

  const toggleDrawer = (open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    )
      return;
    setDrawerState(open);
  };

  const appHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);
  };

  useEffect(() => {
    window.addEventListener("resize", appHeight);
    appHeight();

    // socket.on("receive-telemetry", (data) => {
    //   setMemory(data);
    //   console.log("memory app", data);
    // });

    // socket.on("receive-logs", (data) => {
    //   setLogs(data);
    //   console.log("logs app", data);
    // });

    // socket.on("receive-settings", (data) => {
    //   setSettings(data);
    //   console.log("settings app", data);
    // });

    //TODO: add notification listener
  }, [setLogs, setMemory, setSettings, socket]);

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
        <div className="flex h-16 primary google-shadow z-10">
          <div className="h-full w-16 block md:hidden">
            <div className="flex h-full">
              <div className="m-auto">
                <IconButton onClick={toggleDrawer(true)}>
                  <MenuIcon className="text" />
                </IconButton>
              </div>
            </div>
          </div>
          <div className="flex flex-1 h-full">
            <div className="my-auto ml-0 md:ml-8">
              <h1 className="text-xl font-normal text select-none">
                Telemetry Server
              </h1>
            </div>
          </div>
          <div className="flex h-full w-16">
            <div className="m-auto">
              <DropDown />
            </div>
          </div>
        </div>
        <div className="flex flex-1 min-h-0">
          <div className="flex-none w-60 hidden md:block secondary">
            <SideBar />
          </div>
          <div className="flex flex-col flex-1 secondary">
            <div className="flex-1 overflow-y-auto">{children}</div>
          </div>
        </div>
      </div>
    </>
  );
}
