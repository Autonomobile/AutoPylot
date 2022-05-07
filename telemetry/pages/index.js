import { useState, useEffect } from "react";
import Head from "next/head";
import { VictoryArea, VictoryChart, VictoryAxis, VictoryLine } from "victory";
import { useAtom } from "jotai";
import { memoryAtom } from "../utils/atoms";

export default function Home() {
  const [size, setSize] = useState([0, 0]);
  const [memory, setMemory] = useAtom(memoryAtom);

  const [ramUsage, setRamUsage] = useState([]);
  const [cpuUsage, setCpuUsage] = useState([]);
  const [speed, setSpeed] = useState([]);
  const [steering, setSteering] = useState([]);
  const [throttle, setThrottle] = useState([]);

  useEffect(() => {
    const elem = document.getElementById("model");
    setSize([elem.offsetWidth, elem.offsetHeight]);

    window.addEventListener("resize", () => {
      setSize([elem.offsetWidth, elem.offsetHeight]);
    });
  }, []);

  useEffect(() => {
    if (memory) {


      if (memory.ram_usage){
        ramUsage.push(memory.ram_usage);
        setRamUsage(ramUsage.slice(-100));
      }

      if (memory.cpu_usage){
        cpuUsage.push(memory.cpu_usage);
        setCpuUsage(cpuUsage.slice(-100));
      }

      if (memory.speed){
        speed.push(memory.speed);
        setSpeed(speed.slice(-100));
      }

      if (memory.throttle){
        throttle.push(memory.throttle);
        setThrottle(throttle.slice(-100));
      }

      if (memory.steering){
        steering.push(memory.steering);
        setSteering(steering.slice(-100));
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [memory]);

  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>
      <div className="grid lg:grid-cols-2 p-2">
        <div id="model" className="h-96 p-2">
          <div className="h-full flex flex-col primary">
            <div className="pt-4">
              <p className="text-black text-center">Steering</p>
            </div>

            <div className="flex-1 min-h-0 w-full">
              <VictoryChart width={size[0]} height={size[1]} padding={{ top: 5, bottom: 20, left: 10, right: 0 }}>
                <VictoryAxis dependentAxis tickValues={[-1, -0.5, 0, 0.5, 1]}/>

                <VictoryLine
                  domain={{ y: [-1, 1] }}
                  // interpolation="natural"
                  style={{
                    data: {
                      stroke: "lightgreen",
                      strokeWidth: 2,
                    },
                  }}
                  data={steering}
                />
              </VictoryChart>
            </div>
          </div>
        </div>
        <div className="h-96 p-2">
          <div className="h-full flex flex-col primary">
            <div className="pt-4">
              <p className="text-black text-center">Throttle</p>
            </div>

            <div className="flex-1 min-h-0 w-full">
              <VictoryChart width={size[0]} height={size[1]} padding={{ top: 5, bottom: 20, left: 10, right: 0 }}>
                <VictoryAxis dependentAxis tickValues={[0, 0.5, 1]}/>

                <VictoryArea
                  domain={{ y: [0, 1] }}
                  interpolation="natural"
                  tickFormat={() => ""}
                  style={{
                    data: {
                      // fill: "lightgreen",
                      stroke: "lightgreen",
                      strokeWidth: 2,
                    },
                  }}
                  data={throttle}
                />
              </VictoryChart>
            </div>
          </div>
        </div>
        <div className="h-96 p-2">
          <div className="h-full flex flex-col primary">
            <div className="pt-4">
              <p className="text-black text-center">Speed</p>
            </div>
            <div className="flex-1 min-h-0 w-full">
              <VictoryChart width={size[0]} height={size[1]} padding={{ top: 5, bottom: 20, left: 10, right: 0 }}>
                <VictoryAxis dependentAxis tickValues={[0, 0.5, 1, 1.5, 2]}/>

                <VictoryArea
                  domain={{ y: [0, 5] }}
                  interpolation="natural"
                  tickFormat={() => ""}
                  style={{
                    data: {
                      // fill: "lightgreen",
                      stroke: "lightgreen",
                      strokeWidth: 2,
                    },
                  }}
                  data={speed}
                />
              </VictoryChart>
            </div>
          </div>
        </div>

        <div className="h-96 flex flex-col p-2">

        <div className="h-40 flex flex-col flex-1 primary mb-2">
            <div className="pt-3">
              <p className="text-black text-center">CPU Usage</p>
            </div>
            <div className="flex-1 min-h-0 w-full">
              <VictoryChart width={size[0]} height={size[1] / 2.3} 
                padding={{ top: 5, bottom: 20, left: 0, right: 0 }}
              >
                <VictoryAxis dependentAxis/>
                <VictoryArea
                  domain={{ y: [0, 100] }}
                  interpolation="natural"
                  tickFormat={() => ""}
                  style={{
                    data: {
                      // fill: "lightgreen",
                      stroke: "lightgreen",
                      strokeWidth: 2,
                    },
                  }}
                  data={cpuUsage}
                />
              </VictoryChart>
            </div>
          </div>


          <div className="h-40 flex flex-col flex-1 primary mt-2">
            <div className="pt-3">
              <p className="text-black text-center">RAM Usage</p>
            </div>
            <div className="flex-1 min-h-0 w-full">
              <VictoryChart width={size[0]} height={size[1] / 2.3} 
                padding={{ top: 5, bottom: 20, left: 0, right: 0 }}
              >
                <VictoryAxis dependentAxis/>
                <VictoryArea
                  domain={{ y: [0, 100] }}
                  interpolation="natural"
                  tickFormat={() => ""}
                  style={{
                    data: {
                      // fill: "lightgreen",
                      stroke: "lightgreen",
                      strokeWidth: 2,
                    },
                  }}
                  data={ramUsage}
                />
              </VictoryChart>
            </div>
          </div>

        </div>
      </div>
    </>
  );
}
