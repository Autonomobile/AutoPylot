import "../styles/globals.css";
import { Provider } from "jotai";
import { socketAtom } from "../utils/store";


function MyApp({ Component, pageProps }) {
  const { initialState } = pageProps;
  return (
    <Provider initialValues={initialState && [[socketAtom, initialState]]}>
    <Component {...pageProps} />
  </Provider>
  );
}

export default MyApp;
