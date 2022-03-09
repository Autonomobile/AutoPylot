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
        <h1 className="h text-center mb-12">By Autonomobile</h1>
        <h2>
          <a
            href="https://github.com/Autonomobile/AutoPylot"
            className="underline text-blue-500 hover:text-blue-400 f"
          >
            See the project on Github
          </a>
        </h2>
        <h2 className="mt-5">
          <a
            href="https://github.com/Autonomobile/AutoPylot/raw/telemetry-server/ressources/first-presentation/project-report/project-report.pdf"
            className="underline text-blue-500 hover:text-blue-400 f"
          >
            Download Project Specifications
          </a>
        </h2>
      </div>
    </div>
  );
};
