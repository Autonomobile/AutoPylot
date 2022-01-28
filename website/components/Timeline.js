// @ts-check
import { Document, Page, pdfjs } from "react-pdf";
import { Chrono } from "react-chrono";
import { useEffect, useState } from "react";

pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export const Timeline = () => {
  const [width, setWidth] = useState(0);

  const items = [
    {
      title: "January 17/23th",
      cardTitle: "Starting Project",
      cardDetailedText: "TODO ADD TEXT",
      media: {
        type: "IMAGE",
        source: {
          url: "/logo.svg",
        },
      },
    },
    {
      title: "January 24/30th",
      cardTitle: "Starting Project",
      cardDetailedText: "TODO ADD TEXT",
      media: {
        type: "IMAGE",
        source: {
          url: "/images/github.svg",
        },
      },
    },
  ];

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [width]);

  return (
    <div className="flex w-screen bg-gray-50">
      <div className="mt-12 mx-auto w-full sm:w-2/4 md:w-3/4 lg:w-3/5 h-full">
        <h1 className="h text-center mb-3 mx-12">Timeline</h1>
        <Chrono
          items={items}
          mode={width < 900 ? "VERTICAL" : "VERTICAL_ALTERNATING"}
          scrollable={{ scrollbar: false }}
          hideControls={true}
          theme={{
            primary: "black",
            secondary: "lightblue",
            titleColor: "black",
          }}
        ></Chrono>
      </div>
    </div>
  );
};
