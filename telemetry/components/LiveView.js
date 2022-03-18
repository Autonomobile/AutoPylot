import React from "react";
import { useAtom } from "jotai";
import { memAtom } from "../utils/mem";
import Ratio from "react-ratio";

const LiveView = () => {
  const [mem, setMem] = useAtom(memAtom);

  const base64toImg = (base64) => "data:image/jpeg;base64," + base64;


  return <div>LiveView</div>;
};

export default LiveView;
