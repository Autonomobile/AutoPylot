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
    <FormControl
      sx={{ m: 1, minWidth: 120 }}
    >
      <Select
        value={age}
        onChange={handleChange}
        displayEmpty
        inputProps={{ "aria-label": "Without label" }}
        sx={{
          // remove the default blue border on focus
          border: "none",
          borderBottom: "1px solid",
          borderColor: "gray.300",
          "&:focus": {
            borderColor: "gray.300",
            outline: "none",
          },
          "& $notchedOutline": {
            borderWidth: 0
          },
          "&:hover $notchedOutline": {
            borderWidth: 0
          },
          "&$focused $notchedOutline": {
            borderWidth: 0
          }
        }}
        MenuProps={{
          sx: {
            "&& .Mui-selected": {
              backgroundColor: "#292929"
            },
            // same but with hover effect:
            "&&:hover .Mui-selected": {
              backgroundColor: "#292929"
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
