import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export const Info = () => {
  return (
    <div className="flex w-screen h-screen bg-gray-50">
      <div className="mt-12 mx-auto">
        <h1 className="h text-center">About this Project</h1>
      </div>
    </div>
  );
};
