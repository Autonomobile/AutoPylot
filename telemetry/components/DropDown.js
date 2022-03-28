import { useState, useEffect } from "react";

import { useAtom } from "jotai";
import { carsAtom, carAtom, socketAtom } from "../utils/atoms";

import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

export default function NativeSelectDemo() {
  const [socket] = useAtom(socketAtom);
  const [cars, setCars] = useAtom(carsAtom);
  const [car, setCar] = useAtom(carAtom);
  const [age, setAge] = useState("");
  useEffect(() => {
    socket.on("GET-CARS", (data) => {
      console.log("car test", data);
      setCars(data);
    });
    socket.emit("GET-CARS");
  }, [setCar, setCars, socket]);

  useEffect(() => {
    console.log("cars update", cars);
    if (car === "") {
      if (cars.length === 0) {
        setCar("");
      } else {
        setCar(cars[0]);
      }
    }
    console.log("car update", car);
  }, [car, cars, setCar]);

  function handleChange(event) {
    setCar(event.target.value);
    setAge(event.target.value);
  }

  return (
    <FormControl>
      <Select
        value={age}
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
        {cars.map((car) => (
          <MenuItem key={car} value={car}>
            {car}
          </MenuItem>
        ))}
        <MenuItem value={10}>Ten</MenuItem>
        <MenuItem value={20}>Twenty</MenuItem>
        <MenuItem value={30}>Thirty</MenuItem>
      </Select>
    </FormControl>
  );
}
