import { useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import Head from "next/head";
import { useAtom } from "jotai";
import { settingsAtom, socketAtom, carAtom } from "../utils/atoms";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

import Button from "@mui/material/Button";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import SaveAltIcon from "@mui/icons-material/SaveAlt";

export default function Settings() {
  const [settings, setSettings] = useAtom(settingsAtom);
  const [socket] = useAtom(socketAtom);
  const [car] = useAtom(carAtom);
  const editorRef = useRef(null);

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.setValue(JSON.stringify(settings, null, 4));
    }
  }, [settings]);

  useEffect(() => {
    const editor = document.getElementById("editor");
    editor.addEventListener("keydown", (e) => {
      if (e.key === "s" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        save();
        console.log("SAVING...");
      }
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  function restart() {
    socket.emit("RESTART", car);
  }

  function stop() {
    socket.emit("STOP", car);
    console.log("STOPPING...");
  }

  function save() {
    try {
      if (car !== "") {
        const newSettings = JSON.parse(editorRef.current.getValue());
        setSettings(newSettings);
        console.log("SET_SETTINGS", newSettings);
        socket.emit("SET_SETTINGS", newSettings);
      }
    } catch (e) {
      console.log(e);
    }
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
            sx={{
              backgroundColor: "#d32f2f !important",
              color: "white",
              "&:hover": {
                backgroundColor: "#b71c1c !important",
              },
            }}
          >
            Restart
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={stop}
            startIcon={<PowerSettingsNewIcon />}
            sx={{
              marginLeft: "1rem",
              backgroundColor: "#d32f2f !important",
              color: "white",
              "&:hover": {
                backgroundColor: "#b71c1c !important",
              },
            }}
          >
            Stop
          </Button>
          <Button
            variant="contained"
            color="success"
            onClick={save}
            startIcon={<SaveAltIcon />}
            sx={{
              marginLeft: "1rem",
              backgroundColor: "#2e7d32 !important",
              color: "white",
              "&:hover": {
                backgroundColor: "#1b5e20 !important",
              },
            }}
          >
            Save
          </Button>
        </div>
        <div id="editor" className="h-full">
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
          />
        </div>
      </div>
    </>
  );
}
