import React from "react";
import { useAtom } from "jotai";
import memoryAtom from "../utils/memory";
import Ratio from "react-ratio";
import Skeleton from "@mui/material/Skeleton";

const LiveView = () => {
  const [memory] = useAtom(memoryAtom);

  return (
    <Ratio
      ratio={4 / 3}
      className="w-full md:w-11/12 lg:w-10/12 xl:w-9/12 2xl:w-8/12 hd:w-7/12 uhd:w-6/12 mx-auto 2xl:mx-0"
    >
      {memory.image ? (
        <img src={"data:image/jpeg;base64," + memory.image} alt="live" className="w-full h-full" />
      ) : (
        <Skeleton
          sx={{ bgcolor: "grey.300" }}
          animation="wave"
          variant="rectangular"
          className="w-full h-full"
        />
      )}
    </Ratio>
  );
};

export default LiveView;
