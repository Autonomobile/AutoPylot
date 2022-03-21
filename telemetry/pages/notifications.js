import Alert from "@mui/material/Alert";
import { useAtom } from "jotai";
import notificationsAtom from "../utils/notificationsAtom";

export default function Notifications() {
  const [notifications, setNotifications] = useAtom(notificationsAtom);
  
  function handleClose(index) {
    notifications.splice(index, 1);
    setNotifications([...notifications]);
  }

  return (
    <div className="p-5">
      {notifications.map((notification, index) => (
        <Alert
          key={index}
          severity={notification.severity}
          onClose={() => handleClose(index)}
          className="border-2 mb-4"
        >
          {notification.message}
        </Alert>
      ))}
    </div>
  );
};
