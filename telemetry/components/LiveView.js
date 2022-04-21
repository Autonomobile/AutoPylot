import { useState, useEffect } from "react";
import { useAtom } from "jotai";
import { memoryAtom, carAtom } from "../utils/atoms";
import Ratio from "react-ratio";
import Skeleton from "@mui/material/Skeleton";

const LiveView = () => {
  const [memory] = useAtom(memoryAtom);
  const [image, setImage] = useState("");
  const [car] = useAtom(carAtom);

  useEffect(() => {
    setImage(memory.image);
  }, [memory]);

  function requestFullscreen() {
    var element = document.getElementById("liveview");
    if (element.requestFullscreen) {
      element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
      element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) {
      element.msRequestFullscreen();
    }
  }

  return (
    <Ratio
      id="liveview"
      ratio={4 / 3}
      className="w-full md:w-11/12 lg:w-10/12 xl:w-9/12 xxl:w-8/12 hd:w-7/12 uhd:w-6/12 mx-auto xxl:mx-0 google-shadow"
      onDoubleClick={requestFullscreen}
    >
      {memory.image && car !== "" ? (
        <img
          src={"data:image/jpeg;base64," + image}
          alt="live"
          className="w-full h-full"
        />
      ) : (
        <Skeleton
          sx={{ bgcolor: "#2f2f2f" }}
          animation="wave"
          variant="rectangular"
          className="w-full h-full"
        />
      )}
    </Ratio>
  );
};

export default LiveView;
