import Image from "next/image";
import loader from "../utils/loader";
import Ratio from "react-ratio";

export const Member = (props) => {
  return (
    <Ratio
      className="card flex-0 w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/5 xl:w-1/6 m-3"
      ratio={2 / 3}
    >
      <div className="card-side front bg-transparent w-full h-full">
        <div className="bg-black w-full h-full relative border-2 border-black rounded-lg overflow-hidden">
          <Image
            loader={loader}
            src={props.src}
            alt={props.name}
            layout="fill"
            unoptimized={true}
          />
          <div className="text-black absolute w-full text-center border-b-2 border-black">
            <p className="mini-hc">{props.name}</p>
          </div>
        </div>
      </div>
      <div className="card-side back flex bg-transparent h-full w-full">
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
    </Ratio>
  );
};
