import { Chrono } from "react-chrono";
import { useEffect, useState } from "react";
import {items } from "../data/data";

export const Timeline = () => {
  const [width, setWidth] = useState(0);

  // this function is used to resize the timeline when the window is resized
  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [width]);

  return (
    <div className="flex w-screen bg-gray-50">
      <div className="mt-12 mx-auto w-full sm:w-3/4 md:w-3/4 lg:w-3/5 h-full">
        <h1 className="h text-center mb-3 mx-12">2022 Roadmap</h1>
        <Chrono
          items={items}
          mode={width < 900 ? "VERTICAL" : "VERTICAL_ALTERNATING"}
          scrollable={{ scrollbar: false }}
          hideControls={true}
          theme={{
            primary: "black",
            secondary: "lightblue",
            titleColor: "black",
          }}
        ></Chrono>
      </div>
    </div>
  );
};
