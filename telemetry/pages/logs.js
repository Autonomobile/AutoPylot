import Head from "next/head";
import { useAtom } from "jotai";
import { logsAtom } from "../utils/atoms";
import { DataGrid } from "@mui/x-data-grid";

export default function Logs() {
  const [logs] = useAtom(logsAtom);

  const columns = [
    {
      field: "message",
      headerName: "Message",
      width: 90,
    },
    {
      field: "levelname",
      headerName: "Level",
      width: 90,
    },
    {
      field: "filename",
      headerName: "File Name",
      width: 170,
    },
    {
      field: "funcName",
      headerName: "Func Name",
      width: 90,
    },
    {
      field: "lineno",
      headerName: "Line",
      width: 50,
    },
    {
      field: "processName",
      headerName: "Process Name",
      width: 130,
    },
    {
      field: "process",
      headerName: "Process ID",
      width: 90,
    },
    {
      field: "threadName",
      headerName: "Thread Name",
      width: 150,
    },
    {
      field: "thread",
      headerName: "Thread",
      width: 150,
    },
    {
      field: "asctime",
      headerName: "Asctime",
      width: 190,
    },
  ];

  return (
    <>
      <Head>
        <title>Logs</title>
      </Head>
      <div className="h-full w-full p-10 max-w-full text-white">
        <div
          style={{ height: "100%", width: "100%", backgroundColor: "#2e2f30" }}
        >
          <DataGrid
            rows={logs}
            columns={columns}
            pageSize={100}
            rowsPerPageOptions={[100]}
            checkboxSelection
            sx={{
              height: "100%",
              width: "100%",
              color: "white",
              "&.MuiCheckbox-root": {
                color: "white",
              },
              ".MuiTablePagination-displayedRows": {
                color: "white",
              },
              ".MuiDataGrid-row:hover": {
                backgroundColor: "#121212",
              },
              ".MuiDataGrid-row Mui-selected": {
                backgroundColor: "#121212",
              },
              ".MuiButtonBase-root": {
                color: "white",
              },
              ".MuiTableCell-head": {
                color: "white",
              },
              "&.MuiDataGrid-root .MuiDataGrid-cell:focus": {
                outline: "none",
              },
              ".MuiDataGrid-virtualScroller": {
                backgroundColor: "#121212",
              },
            }}
          />
        </div>
      </div>
    </>
  );
}
