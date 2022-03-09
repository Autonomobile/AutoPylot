import React from "react";
import MenuIcon from "@mui/icons-material/Menu";
import { IconButton } from "@mui/material";
import { useWindowSize } from "../utils/size";
import { Drawer } from "@mui/material";
export const Dash = () => {
  const [state, setState] = React.useState(false);

  const toggleDrawer = (open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setState(open);
  };

  const list = (anchor) => (
    <SideMenu/>
  );

  return (
    <div className="flex flex-col max-h-screen min-h-screen">
      <div className="h-16 flex bg-white drop-shadow-md">
        <div className="w-16 block md:hidden bg-inherit">
          <div className="flex h-full">
            <div className="m-auto">
              <IconButton onClick={toggleDrawer(true)}>
                <MenuIcon />
              </IconButton>
              <Drawer anchor="left" open={state} onClose={toggleDrawer(false)}>
                {list("anchor")}
              </Drawer>
            </div>
          </div>
        </div>
        <div className="flex-1 flex h-full">
          <div className="m-auto">
            <h1 className="scp-font">Telemetry Server</h1>
          </div>
        </div>
      </div>
      <div className="flex-1 h-full flex">
      <div className="min-h-full w-60 bg-red-300 hidden md:block"><SideMenu/></div>
        <div className="min-h-full flex-1 bg-gray-200">test</div>
      </div>
    </div>
  );
};


export const SideMenu = () => {
  return (
    <div className="min-h-full w-60">MENU</div>
  )
}
