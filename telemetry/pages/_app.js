import "../styles/globals.css";
import { Provider } from "jotai";
import { socketAtom } from "../utils/client";
import { useState } from "react";
import MenuIcon from "@mui/icons-material/Menu";
import { IconButton } from "@mui/material";
import { Drawer } from "@mui/material";
import SideBar from "../components/SideBar";
import Head from "next/head";

function TelementryServer({ Component, pageProps }) {
  const { initialState } = pageProps;
  const [drawerState, setDrawerState] = useState(false);

  const toggleDrawer = (open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }
    setDrawerState(open);
  };

  return (
    <Provider initialValues={initialState && [[socketAtom, initialState]]}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="viewport"
          content="initial-scale=1.0, width=device-width"
        ></meta>
      </Head>

      <div className="flex flex-col h-screen">
        <Drawer anchor="left" open={drawerState} onClose={toggleDrawer(false)}>
          <SideBar closeDrawer={() => setDrawerState(false)} />
        </Drawer>
        <div className="flex h-16 bg-gray-600 google-shadow z-10">
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
            <div className="flex-1 overflow-y-auto">
              <Component {...pageProps} />
            </div>
          </div>
        </div>
      </div>
    </Provider>
  );
}

export default TelementryServer;
