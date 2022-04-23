import { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import Head from "next/head";
import { useAtom } from "jotai";
import { settingsAtom } from "../utils/atoms";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export default function Settings() {

  const [settings] = useAtom(settingsAtom);
  const editorRef = useRef(null);

  useEffect(() => {
    if (editorRef.current){
      editorRef.current.setValue(JSON.stringify(settings, null, 4))
    }
  }, [settings]);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor; 
  }

  return (
    <>
      <Head>
        <title>Settings</title>
      </Head>
      <div className="h-full w-full pt-1 scp-font">
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
            onChange={(data, ev) => {
            }}
          />
        </div>
      </div>
    </>
  );
}
