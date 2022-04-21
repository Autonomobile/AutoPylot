// @ts-check
import { useState, useEffect } from "react";

import { useAtom } from "jotai";
import { carsAtom, carAtom, socketAtom, memoryAtom } from "../utils/atoms";

import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

export default function NativeSelectDemo() {
  const [socket] = useAtom(socketAtom);
  const [cars, setCars] = useAtom(carsAtom);
  const [car, setCar] = useAtom(carAtom);


  useEffect(() => {
    socket.on("GET_CARS", (data) => {
      setCars(data)
    });
    socket.emit("GET_CARS");
  }, [socket]);


  useEffect(() => {
    console.log("cars", cars);
    if (!cars.includes(car)) {
      setCar("");
    }
  }, [cars]);

  function handleChange(event) {
    setCar(event.target.value);
    socket.emit("SET_CAR", event.target.value);
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
