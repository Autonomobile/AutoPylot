import React from "react";
import Image from "next/image";

export const Member = (props) => {

  const clickHandler = () => {
    console.log("Clicked on " + props.name);
    console.log(props.bio);
  };

  const size = 200;
  return (
    <div className="w-full sm:w-1/2 lg:w-1/4 relative">
      <div className="p-3 mb-0">
        <div className="bg-white rounded border-black border-2">
          <Image
            className="rounded-t "
            src={props.src}
            alt={props.name}
            layout="responsive"
            width={size}
            height={size * 1.5}
          />
          <div className="border-t-2 border-black hover:cursor-pointer">
            <button className="text-center title w-full text-lg lg:text-sm" onClick={clickHandler}>{props.name}</button>
          </div>
        </div>
      </div>
    </div>
  );
};
