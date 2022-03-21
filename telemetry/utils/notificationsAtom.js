import { atom } from "jotai";

export const notificationsAtom = atom([
  {
    severity: "success",
    message: "This is an success alert — check it out",
  },
  {
    severity: "error",
    message: "This is an error alert — check it out",
  },
  {
    severity: "warning",
    message: "This is an warning alert — check it out",
  },
  {
    severity: "info",
    message: "This is an info alert — check it out",
  },
]);

export default notificationsAtom;