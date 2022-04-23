//@ts-check
import { useAtom } from "jotai";
import { memoryAtom, carAtom } from "../utils/atoms";
import Ratio from "react-ratio";
import Skeleton from "@mui/material/Skeleton";

const LiveView = () => {
  const [memory] = useAtom(memoryAtom);
  const [car] = useAtom(carAtom);

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
    if (car !== "" && memory["image"] !== undefined) {
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
          sx={{ bgcolor: "#2f2f2f", width: "100%", height: "100%" }}
          animation="wave"
          variant="rectangular"
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
