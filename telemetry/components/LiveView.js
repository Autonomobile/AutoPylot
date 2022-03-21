import { useAtom } from "jotai";
import { memoryAtom } from "../utils/atoms";
import Ratio from "react-ratio";
import Skeleton from "@mui/material/Skeleton";

const LiveView = () => {
  const [memory] = useAtom(memoryAtom);

  return (
    <Ratio
      ratio={4 / 3}
      className="w-full md:w-11/12 lg:w-10/12 xl:w-9/12 xxl:w-8/12 hd:w-7/12 uhd:w-6/12 mx-auto xxl:mx-0 google-shadow"
    >
      {memory.image ? (
        <img
          src={"data:image/jpeg;base64," + memory.image}
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
