import HTMLFlipBook from "react-pageflip";
import { Document, Page } from "react-pdf";
import { useState } from "react";

export const Info = () => {

  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  function onError(error) {
    console.log(error);
  }

  return (
    <div className="flex w-screen h-screen bg-gray-50">
      <div className="mt-12 mx-auto">
        <h1 className="h text-center">About this Project</h1>
        {/* <HTMLFlipBook width={300} height={500}>
          
        </HTMLFlipBook> */}

        <div>
      <Document
        file="/public/pdf/test.pdf"
        onLoadSuccess={onDocumentLoadSuccess}
        onLoadError={onError}
      >
        <Page pageNumber={pageNumber} />
      </Document>
      <p>Page {pageNumber} of {numPages}</p>
    </div>
      </div>
    </div>
  );
};
