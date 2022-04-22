//@ts-check
import { useState, useEffect } from "react";
import { useAtom } from "jotai";
import { memoryAtom, carAtom } from "../utils/atoms";
import Ratio from "react-ratio";
import Skeleton from "@mui/material/Skeleton";

const LiveView = () => {
  const [memory] = useAtom(memoryAtom);
  const [display, setDisplay] = useState(false);
  const [car] = useAtom(carAtom);

  useEffect(() => {
    if (car !== "" && memory.hasOwnProperty("image")) {
      setDisplay(true);
    } else {
      setDisplay(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [memory]);

  function requestFullscreen() {
    var element = document.getElementById("liveview");
    if (element.requestFullscreen) {
      element.requestFullscreen();
    }
  }

  function getImage(){
    return "data:image/jpeg;base64," + memory["image"];
  }

  function LiveViewFactory() {
    if (display) {
      return (
        <img
          src={getImage()}
          alt="live"
          className="w-full h-full"
        />
      );
    } else {
      return (
        <Skeleton
          sx={{ bgcolor: "#2f2f2f" }}
          animation="wave"
          variant="rectangular"
          className="w-full h-full"
        />
      );
    }
  }

  return (
    <Ratio
      id="liveview"
      ratio={4 / 3}
      className="w-full md:w-11/12 lg:w-10/12 xl:w-9/12 xxl:w-8/12 hd:w-7/12 uhd:w-6/12 mx-auto xxl:mx-0 google-shadow"
      onDoubleClick={requestFullscreen}
    >
      <LiveViewFactory />
    </Ratio>
  );
};

export default LiveView;
