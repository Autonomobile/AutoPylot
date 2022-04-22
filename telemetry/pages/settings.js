import dynamic from "next/dynamic";
import Head from "next/head";
const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export default function Settings() {
  return (
    <>
      <Head>
        <title>Logs</title>
      </Head>
      <div className="h-full w-full pt-1 scp-font">
        <div className="h-full max-w-full min-w-full">
          <Editor
            height="100%"
            width="100%"
            defaultLanguage="javascript"
            defaultValue="// some comment"
            theme="vs-dark"
            options={{
              scrollBeyondLastLine: false,
              tabSize: 4,
              fontSize: 14,
            }}
          />
        </div>
      </div>
    </>
  );
}
