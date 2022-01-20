import React from "react";
import Image from "next/image";

export const Member = (props) => {
  return (
    <div className="card flex-0 w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/5 xl:w-1/6 aspect-2/3 m-3">
      <div className="card-side front bg-transparent w-full h-full">
        <div className="bg-black w-full h-full relative border-2 border-black rounded-lg overflow-hidden">
          <Image
            className="w-full h-full"
            src={props.src}
            alt={props.name}
            layout="fill"
          />
          <div className="text-black absolute w-full text-center border-b-2 border-black">
            <p className="mini-hc">{props.name}</p>
          </div>
        </div>
      </div>
      <div className="card-side back bg-transparent h-full w-full">
        <div className="bg-white flex flex-col w-full h-full border-2 border-black rounded-lg overflow-hidden">
          <div className="text-black flex-none w-full text-center border-b-2 border-black">
            <p className="mini-hc">{props.login}</p>
          </div>
          <div className="text-black flex flex-1 text-center">
            <div className="m-3">
              <p className="text-center">{props.bio}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

/**
 * 
 *   
 * <div className="flip-card w-full sm:w-1/2 lg:w-1/4 relative p-3 mb-0">
      <div className="flip-card-inner">
        <div className="flip-card-front bg-white rounded-2xl">
          <Image
            className="rounded-t-2xl"
            src={props.src}
            alt={props.name}
            layout="responsive"
            width={300}
            height={500}
          />
          
        </div>
        <div className="flip-card-back bg-red-500">
          <h1>John Doe</h1>
          <p>Architect & Engineer</p>
          <p>We love that guy</p>
        </div>
      </div>
    </div>
 */
