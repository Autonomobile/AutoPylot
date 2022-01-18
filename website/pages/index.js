import Head from "next/head";
import { Brand } from "../components/Brand.js";
import { Members } from "../components/Members.js";
import { Progress } from "../components/Progress.js";
import { Info } from "../components/Info.js";
import { Car } from "../components/Car.js";

export default function Home() {
  return (
    <>
      <Head>
        <title>Autopylot</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>

      <Brand />
      <Car />
      <Members />
      <Info />
      <Progress />
    </>
  );
}
