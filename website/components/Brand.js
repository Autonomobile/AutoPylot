import React from "react";
import Image from "next/image";
import loader from "../utils/loader";

export const Brand = () => {
  return (
    <div className="flex w-screen min-h-screen bg-white text-center">
      <div className="m-auto">
        <Image
            className="rounded-t"
            loader={loader}
            src="logo.svg"
            alt="logo"
            width={250}
            height={250}
            unoptimized={true}
          />
        <h1 className="h text-center">By Autonomobile</h1>
      </div>
    </div>
  );
};
