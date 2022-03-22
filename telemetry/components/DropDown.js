import { useState, useEffect } from "react";

import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import NativeSelect from "@mui/material/NativeSelect";
import { useAtom } from "jotai";
import { carsAtom, carAtom, socketAtom } from "../utils/atoms";
import { CarRental } from "@mui/icons-material";

export default function NativeSelectDemo() {
  const [socket] = useAtom(socketAtom);
  const [cars, setCars] = useAtom(carsAtom);
  const [car, setCar] = useAtom(carAtom);

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
  }

  return (
    <Box sx={{ maxWidth: 40 }}>
      <FormControl fullWidth>
        <NativeSelect
          value={car}
          inputProps={{
            name: "age",
            id: "uncontrolled-native",
          }}
          sx={{
            "&:before": {
              borderColor: "white",
            },
            "&:after": {
              borderColor: "white",
            },
            color: "white",
          }}
          onChange={handleChange}
        >
          <option value={""}>-</option>
          {cars.map((item, index) => (
            <option key={index} value={item}>
              {index + 1}
            </option>
          ))}
        </NativeSelect>
      </FormControl>
    </Box>
  );
}
