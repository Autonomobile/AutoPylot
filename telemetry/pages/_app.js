import { Provider } from "jotai";
import App from "../components/App";
import "../styles/globals.css";

export default function TelementryServer({ Component, pageProps }) {
  return (
    <Provider>
      <App>
        <Component {...pageProps} />
      </App>
    </Provider>
  );
}
