import { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import Head from "next/head";
import { useAtom } from "jotai";
import { settingsAtom, socketAtom, carAtom } from "../utils/atoms";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

import { Button } from "@mui/material";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import SaveAltIcon from "@mui/icons-material/SaveAlt";

export default function Settings() {
  const [settings] = useAtom(settingsAtom);
  const [socket] = useAtom(socketAtom);
  const [car] = useAtom(carAtom);
  const editorRef = useRef(null);

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.setValue(JSON.stringify(settings, null, 4));
    }
  }, [settings]);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  function restart() {
    socket.emit("RESTART", car);
  }

  function save() {
    const newSettings = JSON.parse(editorRef.current.getValue());
    console.log("SET_SETTINGS", newSettings);
    console.log("car", car);
    socket.emit("SET_SETTINGS", newSettings);
  }

  return (
    <>
      <Head>
        <title>Settings</title>
      </Head>
      <div className="h-full w-full flex flex-col">
        <div className="m-4">
          <Button
            variant="contained"
            color="error"
            onClick={restart}
            startIcon={<RestartAltIcon />}
          >
            Restart
          </Button>
          <Button
            variant="contained"
            color="success"
            onClick={save}
            startIcon={<SaveAltIcon />}
            className="ml-4"
          >
            Save
          </Button>
        </div>
        <div className="h-full max-w-full min-w-full">
          <Editor
            height="100%"
            width="100%"
            defaultLanguage="json"
            defaultValue={JSON.stringify(settings, null, 4)}
            theme="vs-dark"
            options={{
              scrollBeyondLastLine: false,
              tabSize: 4,
              fontSize: 14,
            }}
            onMount={handleEditorDidMount}
            onChange={(data, ev) => {}}
          />
        </div>
      </div>
    </>
  );
}
