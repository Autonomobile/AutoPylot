// @ts-check
import { useEffect } from "react";

import { useAtom } from "jotai";
import { carsAtom, carAtom, socketAtom, settingsAtom } from "../utils/atoms";

import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

export default function NativeSelectDemo() {
  const [socket] = useAtom(socketAtom);
  const [cars, setCars] = useAtom(carsAtom);
  const [car, setCar] = useAtom(carAtom);
  const [settings, setSettings] = useAtom(settingsAtom);

  useEffect(() => {
    socket.on("GET_CARS", (data) => {
      setCars(data)
      console.log("GET_CARS :", data);
    });
    socket.emit("GET_CARS");
  }, [setCars, socket]);


  useEffect(() => {
    if (!cars.includes(car) && car !== "") {
      setCar("");
      setSettings({"please choose a car": ":)"});
      socket.emit("SET_CAR", "");
      console.log("SET_CAR :", "");
    }
  }, [car, cars, setCar, setSettings, socket]);

  function handleChange(event) {
    const id = event.target.value;
    setCar(id);
    socket.emit("SET_CAR", id);
    console.log("SET_CAR :", id);

    if (id !== "") {
      socket.emit("GET_SETTINGS", id);
      console.log("GET_SETTINGS");
    } else {
      setSettings({"please choose a car": ":)"});
    }
  }

  return (
    <FormControl>
      <Select
        value={car}
        onChange={handleChange}
        displayEmpty
        inputProps={{ "aria-label": "Without label" }}
        sx={{
          border: "none",
          borderBottom: "1px solid #666666",
          backgroundColor: "#121212",
          color: "white",
          height: "40px",
          minWidth: "90px",
          outline: "none",
          "&& > svg": {
            fill: "#b8b8b8",
          },
        }}
        MenuProps={{
          sx: {
            "&& .Mui-selected": {
              backgroundColor: "#121212"
            },
            "&&:hover .Mui-selected": {
              backgroundColor: "#292929"
            },
            "&& .MuiPaper-root": {
              backgroundColor: "#121212",
              color: "white"
            }
          }
        }}
      >
        <MenuItem value="">
          <em>None</em>
        </MenuItem>
        {cars.map((car, index) => (
          <MenuItem key={car} value={car}>
            {index + 1}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
